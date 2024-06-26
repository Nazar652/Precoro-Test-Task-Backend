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
    product = ProductSerializer(read_only=True)

    def create(self, validated_data):
        cart_user_product = CartUserProduct.objects.create(
            user=validated_data['user_id'],
            product=validated_data['product_id'],
            quantity=validated_data.get('quantity', 1)
        )
        return cart_user_product

    def update(self, instance, validated_data):
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.save()
        return instance

    @staticmethod
    def validate_quantity(value):
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1")
        return value

    class Meta:
        model = CartUserProduct
        fields = ['id', 'user_id', 'product_id', 'quantity', 'product']


class OrderProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    @staticmethod
    def validate_quantity(value):
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1")
        return value

    class Meta:
        model = OrderProduct
        fields = ['id', 'product', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'total_price', 'created_at', 'products']


class WishlistSerializer(serializers.ModelSerializer):
    user_id = serializers.HiddenField(default=serializers.CurrentUserDefault())
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    product = ProductSerializer(read_only=True)

    def create(self, validated_data):
        user = validated_data['user_id']
        product = validated_data['product_id']

        if Wishlist.objects.filter(user=user, product=product).exists():
            raise serializers.ValidationError("This product is already in the wishlist")

        wishlist = Wishlist.objects.create(user=user, product=product)
        return wishlist

    class Meta:
        model = Wishlist
        fields = ['id', 'user_id', 'product_id', 'product']


class CommentSerializer(serializers.ModelSerializer):
    user_id = serializers.HiddenField(default=serializers.CurrentUserDefault())
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    user = UserSerializer(read_only=True)

    def create(self, validated_data):
        comment = Comment.objects.create(
            user=validated_data['user_id'],
            product=validated_data['product_id'],
            text=validated_data['text']
        )
        return comment

    class Meta:
        model = Comment
        fields = ['id', 'user_id', 'product_id', 'text', 'created_at', 'user']


class ReplySerializer(serializers.ModelSerializer):
    user_id = serializers.HiddenField(default=serializers.CurrentUserDefault())
    comment_id = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all())
    user = UserSerializer(read_only=True)

    def create(self, validated_data):
        reply = Reply.objects.create(
            user=validated_data['user_id'],
            comment=validated_data['comment_id'],
            text=validated_data['text']
        )
        return reply

    class Meta:
        model = Reply
        fields = ['id', 'user_id', 'comment_id', 'text', 'created_at', 'user']
