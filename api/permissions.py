# api/permissions.py
from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Разрешает изменять данные только администраторам.
    Остальным — только чтение.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Пользователь может редактировать только свои данные.
    Админ — все.
    """

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.user == request.user


class IsBasketOwner(permissions.BasePermission):
    """
    Пользователь может управлять только своей корзиной
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsOrderOwner(permissions.BasePermission):
    """
    Пользователь может видеть только свои заказы
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user