from rest_framework import viewsets, permissions
from rest_framework.pagination import PageNumberPagination

from .models import Record
from .serializers import RecordSerializer
from .permissions import IsOwnerOrReadOnly


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 9
    page_size_query_param = 'page_size'


class RecordViewSet(viewsets.ModelViewSet):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly,)
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Record.objects.filter(user=self.request.user).order_by('-dt_end')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

