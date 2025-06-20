# main/viewsets.py
from rest_framework import viewsets, permissions, filters
from django.contrib.auth import get_user_model
from main.models import Game, Category, Product, Basket, Order, Review
from .serializers import GameSerializer, CategorySerializer, ProductSerializer, \
    UserSerializer, BasketSerializer, OrderSerializer, ReviewSerializer

User = get_user_model()

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Разрешает редактирование только владельцу или администратору
    """
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.user == request.user


class ReadOnly(permissions.BasePermission):
    """
    Полный запрет на запись
    """
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    pagination_class = viewsets.GenericViewSet.pagination_class

    def get_permissions(self):
        if self.request.method not in ['GET']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    pagination_class = viewsets.GenericViewSet.pagination_class

    def get_permissions(self):
        if self.request.method not in ['GET']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    pagination_class = viewsets.GenericViewSet.pagination_class

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email']
    pagination_class = viewsets.GenericViewSet.pagination_class

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAdminUser()]
        elif self.action in ['create']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]


class BasketViewSet(viewsets.ModelViewSet):
    serializer_class = BasketSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['product__name']
    pagination_class = viewsets.GenericViewSet.pagination_class

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Basket.objects.all()
        return Basket.objects.filter(user=user)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [IsOwnerOrAdmin()]


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['status']
    pagination_class = viewsets.GenericViewSet.pagination_class

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Order.objects.all()
        return Order.objects.filter(user=user)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['comment']
    pagination_class = viewsets.GenericViewSet.pagination_class

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Review.objects.all()
        return Review.objects.filter(user=user)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]