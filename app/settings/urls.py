from rest_framework.routers import DefaultRouter
from .views import SettingsViewSet

router = DefaultRouter()
router.register(r"settings", SettingsViewSet, basename="settings")
router.register(r"about", AboutViewSet, basename="about")
router.register(r"services", ServicesViewSet, basename="services")

urlpatterns = router.urls
