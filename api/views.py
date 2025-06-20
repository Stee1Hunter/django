# api/views.py
from rest_framework import viewsets
from .serializers import GameSerializer, CategorySerializer, ProductSerializer, \
    UserSerializer, BasketSerializer, OrderSerializer, ReviewSerializer
from main.models import Game, Category, Product, User, Basket, Order, Review
from .permissions import IsAdminOrReadOnly, IsOwnerOrAdmin, IsBasketOwner, IsOrderOwner
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    BasePermission,
    SAFE_METHODS
)

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


# === Игры ===
class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = StandardResultsSetPagination
    search_fields = ['name']


# === Категории ===
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = StandardResultsSetPagination
    search_fields = ['name']


# === Товары ===
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = StandardResultsSetPagination
    search_fields = ['name']


# === Пользователи ===
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = StandardResultsSetPagination
    search_fields = ['username']

    def get_permissions(self):
        # Только админы могут создавать/редактировать/удалять
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        # Все могут читать
        return [IsAuthenticated()]


# === Корзина ===
class BasketViewSet(viewsets.ModelViewSet):
    serializer_class = BasketSerializer
    pagination_class = StandardResultsSetPagination
    search_fields = ['product__name']

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Basket.objects.all()
        return Basket.objects.filter(user=user)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsBasketOwner()]
        return [IsAdminUser()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# === Заказы ===
class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    pagination_class = StandardResultsSetPagination
    search_fields = ['status']

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Order.objects.all()
        return Order.objects.filter(user=user)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated(), IsOrderOwner()]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAdminUser()]


# === Отзывы ===
class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = StandardResultsSetPagination
    search_fields = ['rating']

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Review.objects.all()
        return Review.objects.filter(user=user)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        elif self.action in ['create']:
            return [IsAuthenticated()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsOwnerOrAdmin()]
        return [IsAdminUser()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)