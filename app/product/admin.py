from django.contrib import admin
from app.product.models import Product, ProductImage, Category

class ImageProductInlin(admin.TabularInline):
    model = ProductImage
    extra = 1 
    verbose_name = "Фото Продукта"
    verbose_name_plural = "Фото Продукта"

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ImageProductInlin]
    

admin.site.register(Category)