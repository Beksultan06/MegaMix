from django.urls import path, include
from rest_framework.routers import DefaultRouter

from app.product.views import ProductAPI, ToggleFavoriteViewSet, FavoriteListViewSet, OrderViewSet, OrderCreateViewSet, ContactAPI

router = DefaultRouter()
router.register(r"product", ProductAPI, basename='product')
router.register(r'favorites/toggle', ToggleFavoriteViewSet, basename='toggle-favorite')
router.register(r'favorites', FavoriteListViewSet, basename='favorite')
router.register(r'orders', OrderViewSet, basename='orders')
router.register(r'orders/create', OrderCreateViewSet, basename='order-create')
router.register(r"contact", ContactAPI, basename='contact')


urlpatterns = [
    path("", include(router.urls))
]
