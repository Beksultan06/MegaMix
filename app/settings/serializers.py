from rest_framework import serializers
from app.settings.models import Settings, ImageBanner, About, Services


class ImageBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageBanner
        fields = ("id", "image")


class SettingsSerializer(serializers.ModelSerializer):
    banners = ImageBannerSerializer(many=True, read_only=True)

    class Meta:
        model = Settings
        fields = (
            "id",
            "logo",
            "title",
            "description",
            "description2",
            "slide_bar",
            "title_new",
            "description_new",
            "popular_title",
            "popular_description",
            "title_catalog",
            "description_catalog",
            "review_title",
            "description_review",
            "banners",
        )

class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = About
        fields = (
            "id",
            "title",
            "description",
            "image_banner",
            "image",
            "title2",
            "description2",
            "title_services",
            "image1",
            "image2",
            "image3",
        )


class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = (
            "id",
            "title",
            "description",
        )