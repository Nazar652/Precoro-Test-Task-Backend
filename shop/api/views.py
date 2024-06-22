from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .serializers import *

from rest_framework import viewsets, status


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'


class CartUserProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = CartUserProduct.objects.all()
    serializer_class = CartUserProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'

    def get_queryset(self):
        if self.request.user.is_staff:
            return CartUserProduct.objects.all()
        return CartUserProduct.objects.filter(user_id=self.request.user)


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all().prefetch_related('products')
        return Order.objects.filter(user_id=self.request.user).prefetch_related('products')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def make_order(request):
    cart_items = CartUserProduct.objects.filter(user_id=request.user)
    if not cart_items:
        return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

    total_price = 0
    for item in cart_items:
        total_price += item.product.price * item.quantity

    order = Order.objects.create(user=request.user, total_price=total_price)
    for item in cart_items:
        OrderProduct.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )
        item.delete()
    serializer = OrderSerializer(order)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
