from django.contrib import admin
from django.urls import path, include
from .views import redirect_index_view, StartPageView, IndexView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include("myauth.urls")),
    path('', IndexView.as_view(), name='index'),
    path('channels/', include('channels.urls')),
    path('feedback/', include('feedback.urls')),
    path('startpage/', StartPageView.as_view(), name='startpage'),
]
