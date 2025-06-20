from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GameViewSet, CategoryViewSet, ProductViewSet, \
    UserViewSet, BasketViewSet, OrderViewSet, ReviewViewSet

router = DefaultRouter()
router.register(r'games', GameViewSet, basename='game')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'users', UserViewSet, basename='user')
router.register(r'baskets', BasketViewSet, basename='basket')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'reviews', ReviewViewSet, basename='review')

urlpatterns = [
    path('', include(router.urls)),
]