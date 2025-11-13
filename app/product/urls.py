from app.product.views import (
    ProductAPI, ToggleFavoriteViewSet, FavoriteListViewSet,
    OrderViewSet, OrderCreateViewSet, ContactAPI,
    CartListViewSet, CartAddViewSet, CartRemoveViewSet
)

from rest_framework.routers import DefaultRouter
from django.urls import path, include

router = DefaultRouter()
router.register(r"product", ProductAPI, basename='product')
router.register(r'favorites/toggle', ToggleFavoriteViewSet, basename='toggle-favorite')
router.register(r'favorites', FavoriteListViewSet, basename='favorite')
router.register(r'cart', CartListViewSet, basename='cart')              
router.register(r'cart/add', CartAddViewSet, basename='cart-add')       
router.register(r'cart/remove', CartRemoveViewSet, basename='cart-remove')
router.register(r'orders', OrderViewSet, basename='orders')
router.register(r'orders/create', OrderCreateViewSet, basename='order-create')
router.register(r"contact", ContactAPI, basename='contact')

urlpatterns = [
    path("", include(router.urls))
]
