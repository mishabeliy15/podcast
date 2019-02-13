from django.urls import path
from .views import UserCreateAPI, CreateProfile_ByAPI, LogView
from django.contrib.auth import views

app_name = "myauth"

urlpatterns = [
    path('register/', CreateProfile_ByAPI.as_view(), name="reg"),
    path('login/', LogView.as_view(), name="login"),
    path('logout/',views.LogoutView.as_view(),name='logout'),
    path('api/create/',UserCreateAPI.as_view(),name="create-api"),
]