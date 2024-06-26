from django.urls import path, include

from rest_framework import routers

from .views import *

router = routers.SimpleRouter()
router.register(r'users', UserViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'cart', CartUserProductViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'wishlist', WishlistViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'replies', ReplyViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('make-order/', make_order, name='make_order'),
]
