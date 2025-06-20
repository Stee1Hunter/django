# main/api/mixins.py
from django.conf import settings
from rest_framework.exceptions import PermissionDenied

class MethodRestrictionsMixin:
    def get_model_name(self):
        return f"{self.model._meta.app_label}.{self.model.__name__.lower()}"

    def get_method_restrictions(self):
        global_restrictions = getattr(settings, 'REST_FRAMEWORK_METHOD_RESTRICTIONS', {})
        model_name = self.get_model_name()
        restrictions = global_restrictions.get('*', {}).copy()
        if model_name in global_restrictions:
            restrictions.update(global_restrictions[model_name])
        return restrictions

    def is_method_allowed(self, method):
        method = method.lower()
        disabled = self.get_method_restrictions().get('disable_methods', [])
        return method not in disabled

    def http_method_not_allowed(self, request, *args, **kwargs):
        return Response({
            'detail': f'Метод {request.method} не разрешён для этой модели.',
            'allowed_methods': self._get_allowed_methods(),
            'model': self.get_model_name()
        }, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def dispatch(self, request, *args, **kwargs):
        method = request.method.lower()
        if not self.is_method_allowed(method):
            return self.http_method_not_allowed(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)

    def _get_allowed_methods(self):
        disabled = self.get_method_restrictions().get('disable_methods', [])
        return [m.upper() for m in ['get', 'post', 'put', 'patch', 'delete'] if m not in disabled]