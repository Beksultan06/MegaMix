from django.db import models
import uuid
from django.db.models import Sum, F
from django.utils.timezone import now
from datetime import timedelta

class Category(models.Model):
    title = models.CharField(
        max_length=155,
        verbose_name='Категорий'
    )
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категорий'
        verbose_name_plural = 'Категорий'

class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name="category", 
        blank=True, null=True
    )
    title = models.CharField(
        max_length=155,
        verbose_name='Заголовок'
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    price = models.CharField(
        max_length=155,
        verbose_name='Цена'
    )
    price_discount = models.CharField(
        max_length=155,
        verbose_name='Скидка'
    )
    main_params = models.TextField(
        verbose_name='Основные параметры'
    )
    sound_and_features = models.TextField(
        verbose_name='Звук и функции'
    )
    battery_and_power_supply = models.TextField(
        verbose_name='Аккумулятор и питание'
    )
    additionally = models.TextField(
        verbose_name='Дополнительно'
    )
    text = models.TextField(
        verbose_name='Доп Информация'
    )
    sku = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        verbose_name='Артикул',
        blank=True, null=True
    )

    def save(self, *args, **kwargs):
        if not self.sku:
            self.sku = f"PRD-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def total_sold_quantity(self):
        return sum(item.quantity for item in self.orderitem_set.all())
    
    def total_revenue(self):
        try:
            price = float(self.price.replace(',', '.'))
        except:
            price = 0
        return sum(item.quantity * price for item in self.orderitem_set.all())

    def sales_today(self):
        today = now().date()
        return self.orderitem_set.filter(order__created_at__date=today).aggregate(
            total=Sum('quantity')
        )['total'] or 0

    def sales_week(self):
        today = now().date()
        week_start = today - timedelta(days=today.weekday())  # понедельник
        return self.orderitem_set.filter(order__created_at__date__gte=week_start).aggregate(
            total=Sum('quantity')
        )['total'] or 0

    def sales_month(self):
        today = now().date()
        month_start = today.replace(day=1)
        return self.orderitem_set.filter(order__created_at__date__gte=month_start).aggregate(
            total=Sum('quantity')
        )['total'] or 0

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Продукты'
        verbose_name_plural = 'Продукты'


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name='product'
    )
    image = models.ImageField(
        upload_to='product/',
        verbose_name='Фото Продукта'
    )

    def save(self, *args, **kwargs):
        if self.image:
            self.image = save_image_as_webp(self.image, folder="product")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.id 

    class Meta:
        verbose_name = 'Фото Продукта'
        verbose_name_plural = 'Фото Продукта'    

class Favorite(models.Model):
    token = models.CharField(max_length=255, db_index=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"


class CartItem(models.Model):
    token = models.CharField(max_length=255, db_index=True)  
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Элемент корзины"
        verbose_name_plural = "Элементы корзины"
        unique_together = ('token', 'product')

    def __str__(self):
        return f"{self.product.title} x {self.quantity}"



class Order(models.Model):
    DELIVERY_CHOICES = [
        ('standard', 'Обычная доставка'),
        ('scheduled', 'Запланированная доставка'),
    ]

    token = models.CharField(max_length=255, db_index=True) 
    full_name = models.CharField(max_length=155, verbose_name='Имя и Фамилия')
    email = models.EmailField(verbose_name='Почта')
    phone_number = models.CharField(max_length=20, verbose_name='Номер телефона')
    delivery_type = models.CharField(max_length=20, choices=DELIVERY_CHOICES, verbose_name='Тип доставки')
    scheduled_date = models.DateField(null=True, blank=True, verbose_name='Дата доставки')
    scheduled_time = models.TimeField(null=True, blank=True, verbose_name='Время доставки')
    city = models.CharField(max_length=100, verbose_name='Город')
    address = models.CharField(max_length=255, verbose_name='Адрес')
    note = models.TextField(blank=True, verbose_name='Примечание')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Заказ {self.id} - {self.full_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.title} x {self.quantity}"


class Contact(models.Model):
    last_name = models.CharField(
        max_length=155,verbose_name='Фамилия'
    )
    first_name = models.CharField(
        max_length=155,verbose_name='Имя'
    )
    number = models.CharField(
        max_length=25,
        verbose_name='Норер телефона'
    )
    email = models.CharField(
        max_length=155,
        verbose_name='Почта'
    )
    text = models.TextField(
        verbose_name='Сообщение'
    )

    def __str__(self):
        return self.text
    
    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'
