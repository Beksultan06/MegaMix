import uuid
from django.shortcuts import get_object_or_404
from .models import Product, Favorite

def get_or_create_token(request):
    token = request.COOKIES.get('anon_token')
    if not token:
        token = str(uuid.uuid4())
    return token

def toggle_favorite(token, product_id):
    product = get_object_or_404(Product, id=product_id)
    favorite, created = Favorite.objects.get_or_create(token=token, product=product)
    if not created:
        favorite.delete()
        action = "removed"
    else:
        action = "added"
    return action

def get_favorites(token):
    return Favorite.objects.filter(token=token)

def get_or_create_cart_token(request):
    token = request.COOKIES.get('cart_token')
    if not token:
        token = str(uuid.uuid4())
    return token

def add_to_cart(token, product_id, quantity=1):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(token=token, product=product)
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    cart_item.save()
    return cart_item

def remove_from_cart(token, product_id):
    cart_item = get_object_or_404(CartItem, token=token, product_id=product_id)
    cart_item.delete()
    return True

def get_cart_items(token):
    return CartItem.objects.filter(token=token)


def create_order_from_cart(request, order_data):
    token = get_or_create_cart_token(request)
    cart_items = get_cart_items(token)

    order = Order.objects.create(
        token=token,
        full_name=order_data['full_name'],
        email=order_data['email'],
        phone_number=order_data['phone_number'],
        delivery_type=order_data['delivery_type'],
        scheduled_date=order_data.get('scheduled_date'),
        scheduled_time=order_data.get('scheduled_time'),
        city=order_data['city'],
        address=order_data['address'],
        note=order_data.get('note', '')
    )

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity
        )

    cart_items.delete()
    return order