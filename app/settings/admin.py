from django.contrib import admin
from .models import Settings, ImageBanner, About, Services


class ImageBannerInline(admin.TabularInline):
    model = ImageBanner
    extra = 1
    verbose_name = "Фото баннера"
    verbose_name_plural = "Фото баннеров"


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    inlines = [ImageBannerInline]
    list_display = ("title", "slide_bar", "title_catalog")

admin.site.register(About)
admin.site.register(Services)