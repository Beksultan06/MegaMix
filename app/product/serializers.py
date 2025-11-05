from rest_framework import serializers
from app.product.models import Product, ProductImage

class ProductImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ("id", 'image')


class ProductSerializers(serializers.ModelSerializer):
    images = ProductImageSerializers(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'title', 'description', 'price', 'price_discount', 'main_params',
            'sound_and_features', 'battery_and_power_supply', 'additionally', text
        ]