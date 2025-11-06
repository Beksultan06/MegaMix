from django.db import models

from app.utils import save_image_as_webp


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