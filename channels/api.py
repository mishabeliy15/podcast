from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .algorithm import *
from .models import UserPodcast
from .serializers import UserPodcastSerializer
from .permissions import IsOwnerOrReadOnly


@login_required
def search_videosView(request):
    get = request.GET
    res = search_videos(get['video_name'], get['maxResults']) if get['maxResults'] else search_videos(get['name'])
    return JsonResponse(res)

@login_required
def search_videos_view_api2(request):
    get = request.GET
    res = search_videos_API2(get['video_name'], get['maxResults']) if get['maxResults'] else search_videos(get['name'])
    return JsonResponse(res)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 9
    page_size_query_param = 'page_size'


class UserPodcastViewSet(viewsets.ModelViewSet):
    queryset = UserPodcast.objects.all()
    serializer_class = UserPodcastSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly,)
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return UserPodcast.objects.filter(owner=self.request.user).order_by("-added_date")

    @action(detail=True, methods=['patch'], url_name='set_watched')
    def set_watched(self, request, pk=None):
        podcast = self.get_object()
        return Response(self.serializer_class(podcast.watched()).data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'], url_name='listened_n')
    def listened_n(self, request, pk=None):
        podcast = self.get_object()
        n = int(request.data['listen']) if 'listen' in request.data else 15
        return Response(self.serializer_class(podcast.listened_n(15)).data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'], url_name='downloaded')
    def downloaded(self, request, pk=None):
        podcast = self.get_object()
        return Response(self.serializer_class(podcast.downloaded_inc()).data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
