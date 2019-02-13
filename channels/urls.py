from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CreatePodcast, UserPodcastListView, AddPodcastView
from .api import search_videos_view_api2, UserPodcastViewSet

app_name = "channels"

router = DefaultRouter()
router.register(r'user_podcasts', UserPodcastViewSet)

urlpatterns = [
    path('add_by_id/', CreatePodcast.as_view(), name="add_by_id"),
    path('podcast_list/', UserPodcastListView.as_view(), name="podcast_list"),
    path('add_by_name/', AddPodcastView.as_view(), name="add_by_name"),
    path('api/search_videos/', search_videos_view_api2, name='api_search_videos'),
    path('api/', include(router.urls)),
]
