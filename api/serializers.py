from rest_framework import serializers
from main.models import Game, Category, Product, User, Basket, Order, Review

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'name', 'logo_url']


class CategorySerializer(serializers.ModelSerializer):
    game = GameSerializer(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'game']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    game = GameSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'old_price', 'discount', 'image_url', 'category', 'game']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class BasketSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Basket
        fields = ['id', 'user', 'product', 'quantity', 'added_at']


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'user', 'total_price', 'status', 'created_at', 'items']

    def get_items(self, obj):
        return [
            {
                "product": item.product.name,
                "quantity": item.quantity,
                "price": item.price
            }
            for item in obj.orderitem_set.all()
        ]


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'product', 'user', 'rating', 'comment', 'created_at']