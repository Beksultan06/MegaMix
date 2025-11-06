from rest_framework import serializers
from app.product.models import Product, ProductImage, Contact

class ProductImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image"]


class ProductSerializers(serializers.ModelSerializer):
    images = ProductImageSerializers(many=True, read_only=True) 
    category = serializers.StringRelatedField() 

    class Meta:
        model = Product
        fields = [
            'id', 'title', 'description', 'price', 'price_discount', 'main_params',
            'sound_and_features', 'battery_and_power_supply', 'additionally', 'text',
            'category', 'images'  
        ]

class ContactSerializers(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'last_name', 'first_name', 'number', 'email', 'text']