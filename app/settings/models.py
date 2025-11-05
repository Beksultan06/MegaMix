from django.db import models


class Settings(models.Model):
    logo = models.ImageField(
        upload_to='logo',
        verbose_name='Лого'
    )
    title = models.CharField(
        max_length=155,
        verbose_name='Заголовка'
    )
    description = models.TextField(
        verbose_name='Описание Баннера'
    )
    description2 = models.TextField(
        verbose_name='Описание Второй Баннера '
    )
    slide_bar = models.CharField(
        max_length=155,
        verbose_name='Слайд Бар'
    )
    title_new = models.CharField(
        max_length=155,
        verbose_name='Заголовка Новинки'
    )
    description_new = models.TextField(
        verbose_name='Описание Новинки'
    )
    popular_product = models.CharField(
        max_length=155,
        verbose_name='Заголовка Продукты'
    )
    popular_product_text = models.TextField(
        verbose_name='Описание Продукты'
    )
    title_catalog = models.CharField(
        max_length=155,
        verbose_name='Заголовка Каталога'
    )
    description_catalog = models.TextField(
        verbose_name='Описание каталога'
    )
    review_title = models.CharField(
        max_length=155,
        verbose_name='Отзывы'
    )
    description_review = models.TextField(
        verbose_name='Описание отзывов'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Настройки Главной Страницы'
        verbose_name_plural = 'Настройки Главной Страницы'

class ImageBanner(models.Model):
    settings = models.ForeignKey(
        Settings,
        on_delete=models.CASCADE,
        related_name='banners',
        verbose_name='Настройки',
    )
    image = models.ImageField(
        upload_to='image-banner/',
        verbose_name='Фото Баннер'
    )

    class Meta:
        verbose_name = 'Фото Баннера'
        verbose_name_plural = 'Фото Баннера'

    def __str__(self):
        return f"Баннер {self.id}"


class About(models.Model):
    title = models.CharField(
        max_length=155,
        verbose_name='Заголовка о нас'
    )
    description = models.TextField(
        verbose_name='Описание О нас'
    )
    image_banner = models.ImageField(
        upload_to='about',
        verbose_name='Фото о Нас'
    )
    image = models.ImageField(
        upload_to='about',
        verbose_name='Фото '
    )
    title2 = models.CharField(
        max_length=155,
        verbose_name='Под Заголовок'
    )
    description2 = models.TextField(
        verbose_name='Под Описание О нас'
    )
    title_services = models.CharField(
        max_length=155,
        verbose_name='Заголовка Услуги'
    )
    image1 = models.ImageField(
        upload_to='about',
        verbose_name='Фото 1'
    )
    image2 = models.ImageField(
        upload_to='about',
        verbose_name='Фото 2'
    )
    image3 = models.ImageField(
        upload_to='about',
        verbose_name='Фото 3'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Настройки Старницы О нас '
        verbose_name_plural = 'Настройки Старницы О нас '

class Services(models.Model):
    title = models.CharField(
        max_length=155,
        verbose_name='Заголовка'
    )
    description = models.TextField(
        verbose_name='Описание'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Услуги'
        verbose_name_plural = 'Услуги'