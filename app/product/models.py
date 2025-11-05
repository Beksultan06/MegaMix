from django.db import models

class Product(models.Model):
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

    def __str__(self):
        return self.id 

    class Meta:
        verbose_name = 'Фото Продукта'
        verbose_name_plural = 'Фото Продукта'    