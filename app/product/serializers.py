from rest_framework import serializers
from app.product.models import Product, ProductImage, Favorite, OrderItem, Order, CartItem, Contact

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
            'category', 'images', 'sku'
        ]

class FavoriteSerializer(serializers.ModelSerializer):
    product = ProductSerializers(read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'product', 'created_at']

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializers(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'created_at']

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializers(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'full_name', 'email', 'phone_number',
            'delivery_type', 'scheduled_date', 'scheduled_time',
            'city', 'address', 'note', 'created_at', 'items'
        ]

class ContactSerializers(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'last_name', 'first_name', 'number', 'email', 'text']
