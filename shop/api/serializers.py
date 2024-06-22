from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import *

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

    class Meta:
        model = User
        fields = ['id', 'username', 'password']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CartUserProductSerializer(serializers.ModelSerializer):
    user_id = serializers.HiddenField(default=serializers.CurrentUserDefault())
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    def create(self, validated_data):
        cart_user_product = CartUserProduct.objects.create(
            user=validated_data['user_id'],
            product=validated_data['product_id'],
            quantity=validated_data.get('quantity', 1)
        )
        return cart_user_product

    @staticmethod
    def validate_quantity(value):
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1")
        return value

    class Meta:
        model = CartUserProduct
        fields = ['id', 'user_id', 'product_id', 'quantity']


class OrderProductSerializer(serializers.ModelSerializer):
    @staticmethod
    def validate_quantity(value):
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1")
        return value

    class Meta:
        model = OrderProduct
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'total_price', 'created_at', 'products']
