from django.core.cache import cache
from app.product.models import Product

class ProductService:
    CACHE_KEY = "random_products_ids"
    CACHE_TIMEOUT = 300

    @classmethod
    def get_random_products(cls):
        product_ids = cache.get(cls.CACHE_KEY)
        if not product_ids:
            product_ids = list(Product.objects.all().order_by("?").values_list("id", flat=True))
            cache.set(cls.CACHE_KEY, product_ids, cls.CACHE_TIMEOUT)
        return Product.objects.filter(id__in=product_ids)
