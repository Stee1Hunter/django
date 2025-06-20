from django.contrib import admin
from django.contrib.auth.models import User
from .models import Game, Category, Product, Review, Basket, Order, OrderItem

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'logo_url')
    search_fields = ('name',)
    list_filter = ('name',)
    ordering = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name', 'logo_url')
        }),
    )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'game')
    search_fields = ('name', 'game__name')
    list_filter = ('game',)
    ordering = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name', 'game')
        }),
    )

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'game', 'price', 'discount')
    search_fields = ('name', 'category__name', 'game__name')
    list_filter = ('category', 'game', 'discount')
    ordering = ('name',)
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'description', 'category', 'game')
        }),
        ('Цены', {
            'fields': ('price', 'old_price', 'discount')
        }),
        ('Изображение', {
            'fields': ('image_url',)
        }),
    )

@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'created_at')
    search_fields = ('user__username', 'product__name')
    list_filter = ('user', 'created_at')
    ordering = ('-created_at',)
    fieldsets = (
        ('Содержимое корзины', {
            'fields': ('user', 'product', 'quantity')
        }),
        ('Метаданные', {
            'fields': ('created_at',)
        }),
    )

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'status', 'created_at')
    search_fields = ('user__username', 'id')
    list_filter = ('status', 'created_at')
    ordering = ('-created_at',)
    fieldsets = (
        ('Информация о заказе', {
            'fields': ('user', 'total_price', 'status')
        }),
        ('Метаданные', {
            'fields': ('created_at',)
        }),
    )

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')
    search_fields = ('order__id', 'product__name')
    list_filter = ('order', 'product')
    ordering = ('-order',)
    fieldsets = (
        ('Состав заказа', {
            'fields': ('order', 'product', 'quantity', 'price')
        }),
    )

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    search_fields = ('product__name', 'user__username')
    list_filter = ('rating', 'created_at')
    ordering = ('-created_at',)
    fieldsets = (
        ('Содержимое отзыва', {
            'fields': ('product', 'user', 'rating', 'comment')
        }),
        ('Метаданные', {
            'fields': ('created_at',)
        }),
    )