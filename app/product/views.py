from rest_framework import viewsets, mixins, filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.core.cache import cache

from app.product.models import Product, Favorite, Order, Contact
from app.product.serializers import ProductSerializers, FavoriteSerializer, OrderSerializer, CartItemSerializer, ContactSerializers
from app.product.service import ProductService
from app.product.utils import get_or_create_token, toggle_favorite, get_favorites, create_order_from_cart
from app.telegrambot.utils import send_message_to_all

class ProductAPI(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = ProductSerializers
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'price', 'category__title', 'sku']
    filterset_fields = ['category']

    def get_queryset(self):
        return ProductService.get_random_products()


class ToggleFavoriteViewSet(mixins.CreateModelMixin,
                            viewsets.GenericViewSet):
    serializer_class = FavoriteSerializer

    def create(self, request, *args, **kwargs):
        product_id = self.kwargs.get('product_id')
        token = get_or_create_token(request)
        action = toggle_favorite(token, product_id)

        response = Response({"status": "success", "action": action})
        response.set_cookie('anon_token', token, max_age=60*60*24*365)
        return response

class FavoriteListViewSet(mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        token = get_or_create_token(self.request)
        return get_favorites(token)

class CartListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = CartItemSerializer

    def get_queryset(self):
        token = get_or_create_cart_token(self.request)
        return get_cart_items(token)

class CartAddViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = CartItemSerializer

    def create(self, request, *args, **kwargs):
        token = get_or_create_cart_token(request)
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        cart_item = add_to_cart(token, product_id, quantity)
        serializer = self.get_serializer(cart_item)
        response = Response(serializer.data, status=status.HTTP_201_CREATED)
        response.set_cookie('cart_token', token, max_age=60*60*24*365)
        return response

class CartRemoveViewSet(viewsets.GenericViewSet):
    def destroy(self, request, *args, **kwargs):
        token = get_or_create_cart_token(request)
        product_id = kwargs.get('product_id')
        remove_from_cart(token, product_id)
        response = Response({"status": "deleted"}, status=status.HTTP_204_NO_CONTENT)
        response.set_cookie('cart_token', token, max_age=60*60*24*365)
        return response

class OrderViewSet(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    serializer_class = OrderSerializer

    def get_queryset(self):
        token = self.request.COOKIES.get('cart_token')
        if token:
            return Order.objects.filter(token=token)
        return Order.objects.none()

class OrderCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = create_order_from_cart(request, serializer.validated_data)
        output_serializer = self.get_serializer(order)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class ContactAPI(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializers