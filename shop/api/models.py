from django.contrib.auth.models import AbstractUser
from django.db.models import *


class Category(Model):
    name = CharField(max_length=40)
    description = CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


class Product(Model):
    name = CharField(max_length=40)
    description = CharField(max_length=255, null=True, blank=True)
    price = IntegerField()
    category_id = ForeignKey(Category, on_delete=CASCADE)

    def __str__(self):
        return self.name


class User(AbstractUser):
    cart = ManyToManyField(Product, through='CartUserProduct')


class CartUserProduct(Model):
    user_id = ForeignKey(User, on_delete=CASCADE)
    product_id = ForeignKey(Product, on_delete=CASCADE)
    quantity = IntegerField(default=1)


class Order(Model):
    user_id = ForeignKey(User, on_delete=CASCADE)
    total_price = IntegerField()
    created_at = DateTimeField(auto_now_add=True)


class OrderProduct(Model):
    order_id = ForeignKey(Order, on_delete=CASCADE)
    product_id = ForeignKey(Product, on_delete=CASCADE)
    quantity = IntegerField(default=1)
    price = IntegerField()
