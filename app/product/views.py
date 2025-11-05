from rest_framework import viewsets, mixins

from app.product.models import Product, ProductImage 
from app.product.serializers import ProductImageSerializers, ProductSerializers

class ProductAPI(viewsets.GenericViewSet, 
                mixins.ListModelMixin):
    queryset = Product.objects.all().order_by("?")
    serializer_class = ProductSerializers