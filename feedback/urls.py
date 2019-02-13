from django.urls import path
from .views import CreateFeedbackAPI

app_name = "feedback"

urlpatterns = [
    path('api/', CreateFeedbackAPI.as_view(), name="api_create"),
]
