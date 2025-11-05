from rest_framework import mixins, viewsets
from app.settings.models import Settings, About, Services
from app.settings.serializers import SettingsSerializer, AboutSerializer, ServicesSerializer


class SettingsViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet
    ):
    queryset = Settings.objects.all()
    serializer_class = SettingsSerializer


class AboutViewSet(
    mixins.ListModelMixin,      
    mixins.RetrieveModelMixin, 
    viewsets.GenericViewSet
):
    queryset = About.objects.all()
    serializer_class = AboutSerializer


class ServicesViewSet(
    mixins.ListModelMixin,       
    mixins.RetrieveModelMixin,   
    viewsets.GenericViewSet
):
    queryset = Services.objects.all()
    serializer_class = ServicesSerializer
