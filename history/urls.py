from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import RecordViewSet

app_name = "history"

router = DefaultRouter()
router.register(r'record', RecordViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
