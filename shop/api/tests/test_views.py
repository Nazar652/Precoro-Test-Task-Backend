# tests.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from ..models import Category, Product, CartUserProduct, Order, OrderProduct

User = get_user_model()


class UserViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.admin_user = User.objects.create_superuser(username='admin', password='adminpass')

    def test_create_user(self):
        url = reverse('user-list')
        data = {'username': 'newuser', 'password': 'newpass'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)

    def test_get_user_list(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('user-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


class CategoryViewSetTests(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Category 1', description='Description 1')

    def test_get_category_list(self):
        url = reverse('category-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class ProductViewSetTests(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Category 1', description='Description 1')
        self.product = Product.objects.create(name='Product 1', description='Description 1', price=100,
                                              category=self.category)

    def test_get_product_list(self):
        url = reverse('product-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class CartUserProductViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category = Category.objects.create(name='Category 1', description='Description 1')
        self.product = Product.objects.create(name='Product 1', description='Description 1', price=100,
                                              category=self.category)
        self.cart_item = CartUserProduct.objects.create(user=self.user, product=self.product, quantity=2)
        self.client.force_authenticate(user=self.user)

    def test_get_cart_items(self):
        url = reverse('cartuserproduct-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_cart_item(self):
        url = reverse('cartuserproduct-list')
        data = {'product_id': self.product.id, 'quantity': 1}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CartUserProduct.objects.count(), 2)


class OrderViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category = Category.objects.create(name='Category 1', description='Description 1')
        self.product = Product.objects.create(name='Product 1', description='Description 1', price=100,
                                              category=self.category)
        self.client.force_authenticate(user=self.user)

    def test_get_orders(self):
        order = Order.objects.create(user=self.user, total_price=200)
        OrderProduct.objects.create(order=order, product=self.product, quantity=2, price=100)

        url = reverse('order-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_make_order(self):
        CartUserProduct.objects.create(user=self.user, product=self.product, quantity=2)

        url = reverse('make_order')
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderProduct.objects.count(), 1)
