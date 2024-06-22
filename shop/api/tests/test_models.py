from django.test import TestCase
from ..models import Category, Product, User, CartUserProduct, Order, OrderProduct


class TestCategoryModel(TestCase):
    def test_category_model(self):
        category = Category.objects.create(name='Test Category', description='Test Description')
        self.assertEqual(str(category), 'Test Category')


class TestProductModel(TestCase):
    def test_product_model(self):
        category = Category.objects.create(name='Test Category', description='Test Description')
        product = Product.objects.create(name='Test Product', description='Test Description', price=100,
                                         category=category)
        self.assertEqual(str(product), 'Test Product')
        self.assertEqual(product.category, category)


class TestUserModel(TestCase):
    def test_user_model(self):
        user = User.objects.create(username='test_user', password='test_password')
        self.assertEqual(user.username, 'test_user')


class TestCartUserProductModel(TestCase):
    def test_cart_user_product_model(self):
        user = User.objects.create(username='test_user', password='test_password')
        category = Category.objects.create(name='Test Category', description='Test Description')
        product = Product.objects.create(name='Test Product', description='Test Description', price=100,
                                         category=category)
        cart_user_product = CartUserProduct.objects.create(user=user, product=product, quantity=2)
        self.assertEqual(cart_user_product.user, user)
        self.assertEqual(cart_user_product.product, product)
        self.assertEqual(cart_user_product.quantity, 2)


class TestOrderModel(TestCase):
    def test_order_model(self):
        user = User.objects.create(username='test_user', password='test_password')
        order = Order.objects.create(user=user, total_price=100)
        self.assertEqual(order.user, user)
        self.assertEqual(order.total_price, 100)


class TestOrderProductModel(TestCase):
    def test_order_product_model(self):
        user = User.objects.create(username='test_user', password='test_password')
        category = Category.objects.create(name='Test Category', description='Test Description')
        product = Product.objects.create(name='Test Product', description='Test Description', price=100,
                                         category=category)
        order = Order.objects.create(user=user, total_price=100)
        order_product = OrderProduct.objects.create(order=order, product=product, quantity=2, price=100)
        self.assertEqual(order_product.order, order)
        self.assertEqual(order_product.product, product)
        self.assertEqual(order_product.quantity, 2)
        self.assertEqual(order_product.price, 100)
