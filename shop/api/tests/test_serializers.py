from django.contrib.auth import get_user_model
from django.test import TestCase
from ..serializers import (UserSerializer, CategorySerializer, ProductSerializer, CartUserProductSerializer,
                           OrderSerializer, OrderProductSerializer)
from ..models import Category, Product, CartUserProduct, Order, OrderProduct
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory, force_authenticate

factory = APIRequestFactory()

User = get_user_model()


class UserSerializerTest(TestCase):
    def setUp(self):
        self.user_attributes = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        self.user = User.objects.create_user(**self.user_attributes)
        self.serializer = UserSerializer(instance=self.user)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), {'id', 'username'})

    def test_username_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['username'], self.user_attributes['username'])

    def test_password_field_write_only(self):
        data = self.serializer.data
        self.assertNotIn('password', data)

    def test_validation_error_for_empty_username(self):
        invalid_data = {
            'username': '',
            'password': 'testpassword'
        }
        serializer = UserSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), {'username'})

    def test_validation_error_for_empty_password(self):
        invalid_data = {
            'username': 'testuser1',
            'password': ''
        }
        serializer = UserSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), {'password'})

    def test_create_user(self):
        valid_data = {
            'username': 'newuser',
            'password': 'newpassword'
        }
        serializer = UserSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.username, valid_data['username'])
        self.assertTrue(user.check_password(valid_data['password']))


class CategorySerializerTest(TestCase):
    def setUp(self):
        self.category_attributes = {
            'name': 'Test Category',
            'description': 'This is a test category description'
        }
        self.category = Category.objects.create(**self.category_attributes)
        self.serializer = CategorySerializer(instance=self.category)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), {'id', 'name', 'description'})

    def test_name_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['name'], self.category_attributes['name'])

    def test_description_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['description'], self.category_attributes['description'])

    def test_validation_error_for_empty_name(self):
        invalid_data = {
            'name': '',
            'description': 'This is a test category description'
        }
        serializer = CategorySerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), {'name'})

    def test_create_category(self):
        valid_data = {
            'name': 'New Category',
            'description': 'This is a new category description'
        }
        serializer = CategorySerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())
        category = serializer.save()
        self.assertEqual(category.name, valid_data['name'])
        self.assertEqual(category.description, valid_data['description'])


class ProductSerializerTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Test Category',
            description='This is a test category description'
        )
        self.product_attributes = {
            'name': 'Test Product',
            'description': 'This is a test product description',
            'price': 100,
            'category': self.category
        }
        self.product = Product.objects.create(**self.product_attributes)
        self.serializer = ProductSerializer(instance=self.product)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), {'id', 'name', 'description', 'price', 'category'})

    def test_name_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['name'], self.product_attributes['name'])

    def test_description_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['description'], self.product_attributes['description'])

    def test_price_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['price'], self.product_attributes['price'])

    def test_category_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['category'], self.category.id)

    def test_validation_error_for_empty_name(self):
        invalid_data = {
            'name': '',
            'description': 'This is a test product description',
            'price': 100,
            'category': self.category.id
        }
        serializer = ProductSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), {'name'})

    def test_validation_error_for_empty_price(self):
        invalid_data = {
            'name': 'Test Product',
            'description': 'This is a test product description',
            'price': None,
            'category': self.category.id
        }
        serializer = ProductSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), {'price'})

    def test_create_product(self):
        valid_data = {
            'name': 'New Product',
            'description': 'This is a new product description',
            'price': 150,
            'category': self.category.id
        }
        serializer = ProductSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())
        product = serializer.save()
        self.assertEqual(product.name, valid_data['name'])
        self.assertEqual(product.description, valid_data['description'])
        self.assertEqual(product.price, valid_data['price'])
        self.assertEqual(product.category.id, valid_data['category'])


class CartUserProductSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(name='Test Product', price=100, category=self.category)
        self.cart_user_product_attributes = {
            'user_id': self.user.id,
            'product_id': self.product.id,
            'quantity': 2
        }
        request = factory.post('/cart/')
        force_authenticate(request, user=self.user)

        self.serializer_context = {
            'request': Request(request),
        }
        self.cart_user_product = CartUserProduct.objects.create(**self.cart_user_product_attributes)
        self.serializer = CartUserProductSerializer(instance=self.cart_user_product, context=self.serializer_context)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), {'id', 'product_id', 'quantity'})

    def test_product_id_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['product_id'], self.cart_user_product_attributes['product_id'])

    def test_quantity_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['quantity'], self.cart_user_product_attributes['quantity'])

    def test_validation_error_for_quantity_less_than_one(self):
        invalid_data = {
            'user_id': self.user.id,
            'product_id': self.product.id,
            'quantity': 0
        }
        serializer = CartUserProductSerializer(data=invalid_data, context=self.serializer_context)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), {'quantity'})

    def test_create_cart_user_product(self):
        valid_data = {
            'user_id': self.user.id,
            'product_id': self.product.id,
            'quantity': 3
        }
        serializer = CartUserProductSerializer(data=valid_data, context=self.serializer_context)
        self.assertTrue(serializer.is_valid())
        cart_user_product = serializer.save()
        self.assertEqual(cart_user_product.user_id, valid_data['user_id'])
        self.assertEqual(cart_user_product.product_id, valid_data['product_id'])
        self.assertEqual(cart_user_product.quantity, valid_data['quantity'])


class OrderSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.order_attributes = {
            'user': self.user,
            'total_price': 200
        }
        self.order = Order.objects.create(**self.order_attributes)
        self.serializer = OrderSerializer(instance=self.order)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), {'id', 'user', 'total_price', 'created_at', 'products'})

    def test_user_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['user'], self.user.id)

    def test_total_price_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['total_price'], self.order_attributes['total_price'])

    def test_products_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['products'], [])

    def test_create_order(self):
        valid_data = {
            'user': self.user.id,
            'total_price': 300
        }
        serializer = OrderSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())
        order = serializer.save()
        self.assertEqual(order.user.id, valid_data['user'])
        self.assertEqual(order.total_price, valid_data['total_price'])


class OrderProductSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(name='Test Product', price=100, category=self.category)
        self.order = Order.objects.create(user=self.user, total_price=200)
        self.order_product_attributes = {
            'order': self.order,
            'product': self.product,
            'quantity': 2,
            'price': 100
        }
        self.order_product = OrderProduct.objects.create(**self.order_product_attributes)
        self.serializer = OrderProductSerializer(instance=self.order_product)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), {'id', 'order', 'product', 'quantity', 'price'})

    def test_order_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['order'], self.order.id)

    def test_product_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['product'], self.product.id)

    def test_quantity_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['quantity'], self.order_product_attributes['quantity'])

    def test_price_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['price'], self.order_product_attributes['price'])

    def test_validation_error_for_quantity_less_than_one(self):
        invalid_data = {
            'order': self.order.id,
            'product': self.product.id,
            'quantity': 0,
            'price': 100
        }
        serializer = OrderProductSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), {'quantity'})

    def test_create_order_product(self):
        valid_data = {
            'order': self.order.id,
            'product': self.product.id,
            'quantity': 3,
            'price': 100
        }
        serializer = OrderProductSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())
        order_product = serializer.save()
        self.assertEqual(order_product.order.id, valid_data['order'])
        self.assertEqual(order_product.product.id, valid_data['product'])
        self.assertEqual(order_product.quantity, valid_data['quantity'])
        self.assertEqual(order_product.price, valid_data['price'])
