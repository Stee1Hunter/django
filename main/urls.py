from django.urls import path
from .views import (
    IndexView, ProductView, AboutView,
    BasketView, AddToBasketView, RemoveFromBasketView,
    UpdateBasketView, CreateOrderView, AddReviewView,
    ProductCreateView, ProductUpdateView, ProductDeleteView,
    GameCreateView, GameUpdateView, GameDeleteView,
    CategoryCreateView, CategoryUpdateView, CategoryDeleteView,
    UserCreateView, UserUpdateView, UserDeleteView,
    OrderListView, OrderDetailView, OrderUpdateView,
    ReviewListView, ReviewUpdateView, ReviewDeleteView, catalog_view, login_user, registration_user, logout_user, profile_view
    , UserOrdersView, OrderDetailView
)

urlpatterns = [
    # Основные страницы
    path('', IndexView.as_view(), name='index'),
    path('about/', AboutView.as_view(), name='about'),
    path('basket/', BasketView.as_view(), name='basket'),
    path('prodinfo/<int:product_id>/', ProductView.as_view(), name='product'),
    path('catalog/<int:game_id>/', catalog_view, name='catalog'),
    path('profile/', profile_view, name='profile'),
    # Регаистрация и авторизация
    path('login/', login_user, name='login'),
    path('register/', registration_user, name='register'),
    path('logout/', logout_user, name='logout'),
    path('add-to-basket/<int:product_id>/', AddToBasketView.as_view(), name='add_to_basket'),
    path('remove-from-basket/<int:item_id>/', RemoveFromBasketView.as_view(), name='remove_from_basket'),
    path('update-basket/<int:item_id>/', UpdateBasketView.as_view(), name='UpdateBasketView'),
    # отображение заказов
    # Заказы

    path('create-order/', CreateOrderView.as_view(), name='create_order'),  # <-- Вот эта строчка добавлена
    path('my-orders/', UserOrdersView.as_view(), name='my_orders'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    # API endpoints
    path('add-to-basket/<int:product_id>/', AddToBasketView.as_view(), name='add_to_basket'),
    path('remove-from-basket/<int:item_id>/', RemoveFromBasketView.as_view(), name='remove_from_basket'),
    path('update-basket/<int:item_id>/', UpdateBasketView.as_view(), name='update_basket'),
    path('create-order/', CreateOrderView.as_view(), name='create_order'),
    path('add-review/<int:product_id>/', AddReviewView.as_view(), name='add_review'),

    # Товары
    path('product/new/', ProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/edit/', ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),

    # Игры
    path('game/new/', GameCreateView.as_view(), name='game_create'),
    path('game/<int:pk>/edit/', GameUpdateView.as_view(), name='game_update'),
    path('game/<int:pk>/delete/', GameDeleteView.as_view(), name='game_delete'),

    # Категории
    path('category/new/', CategoryCreateView.as_view(), name='category_create'),
    path('category/<int:pk>/edit/', CategoryUpdateView.as_view(), name='category_update'),
    path('category/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),

    # Пользователи
    path('user/new/', UserCreateView.as_view(), name='user_create'),
    path('user/<int:pk>/edit/', UserUpdateView.as_view(), name='user_update'),
    path('user/<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),

    # Заказы
    path('orders/new', OrderListView.as_view(), name='order_list'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('order/<int:pk>/edit/', OrderUpdateView.as_view(), name='order_update'),

    # Отзывы
    path('reviews/new', ReviewListView.as_view(), name='review_list'),
    path('review/<int:pk>/edit/', ReviewUpdateView.as_view(), name='review_update'),
    path('review/<int:pk>/delete/', ReviewDeleteView.as_view(), name='review_delete'),
]