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
    category = ForeignKey(Category, on_delete=CASCADE)
    image = ImageField(default=None, null=True, blank=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    pass


class CartUserProduct(Model):
    user = ForeignKey(User, on_delete=CASCADE)
    product = ForeignKey(Product, on_delete=CASCADE)
    quantity = IntegerField(default=1)


class Order(Model):
    user = ForeignKey(User, on_delete=CASCADE)
    total_price = IntegerField()
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class OrderProduct(Model):
    order = ForeignKey(Order, related_name='products', on_delete=CASCADE)
    product = ForeignKey(Product, on_delete=CASCADE)
    quantity = IntegerField(default=1)
    price = IntegerField()


class Wishlist(Model):
    user = ForeignKey(User, on_delete=CASCADE)
    product = ForeignKey(Product, on_delete=CASCADE)

    class Meta:
        unique_together = ('user', 'product')


class Comment(Model):
    user = ForeignKey(User, on_delete=CASCADE)
    product = ForeignKey(Product, on_delete=CASCADE)
    text = TextField()
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class Reply(Model):
    user = ForeignKey(User, on_delete=CASCADE)
    comment = ForeignKey(Comment, on_delete=CASCADE)
    text = TextField()
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
