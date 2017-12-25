from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from .views import LogsViewSet

router = DefaultRouter()
router.register(r'logs', LogsViewSet, base_name='logs')
urlpatterns = router.urls

