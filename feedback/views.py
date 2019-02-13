from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from .models import Feedback
from .serializers import FeedbackSerializer


class CreateFeedbackAPI(CreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
