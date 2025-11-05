from rest_framework import viewsets, mixins, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.core.cache import cache

from app.product.models import Product
from app.product.serializers import ProductSerializers
from app.product.service import ProductService

class ProductAPI(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = ProductSerializers
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'price', 'category__title']
    filterset_fields = ['category']

    def get_queryset(self):
        return ProductService.get_random_products()