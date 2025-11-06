from django.urls import path, include
from rest_framework.routers import DefaultRouter

from app.product.views import ProductAPI, ContactAPI

router = DefaultRouter()
router.register(r"product", ProductAPI, basename='product')
router.register(r"contact", ContactAPI, basename='contact')


urlpatterns = [
    path("", include(router.urls))
]
