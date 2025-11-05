from django.urls import path, include
from rest_framework.routers import DefaultRouter

from app.product.views import ProductAPI

router = DefaultRouter()
router.register(r"product", ProductAPI, basename='product')

urlpatterns = [
    path("", include(router.urls))
]
