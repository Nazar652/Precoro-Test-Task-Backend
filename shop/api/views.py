from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .filters import ProductFilter
from .serializers import *

from rest_framework import viewsets, status


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ProductFilter
    ordering_fields = ['id', 'price']
    ordering = ['id']


class CartUserProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = CartUserProduct.objects.all()
    serializer_class = CartUserProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user']

    def get_queryset(self):
        if self.request.user.is_staff:
            return CartUserProduct.objects.all()
        return CartUserProduct.objects.filter(user_id=self.request.user)


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user']

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


class WishlistViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product_id']

    def get_queryset(self):
        return Wishlist.objects.filter(user_id=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product_id']

    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)


class ReplyViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['comment_id']

    def destroy(self, request, *args, **kwargs):
        reply = self.get_object()
        if reply.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
