# Create your views here.
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, TemplateView
from .forms import UserModelForm
from django.contrib.auth.models import User
from rest_framework.generics import CreateAPIView
from .serializers import UserSerializer
from podcast.views import check_on_mobile
from django.contrib import messages


class CreateProfile(CreateView):
    success_url = '/'
    model = User
    form_class = UserModelForm
    template_name = 'myauth/reg.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Profile creation'
        context['mobile'] = check_on_mobile(self.request)
        return context


class UserCreateAPI(CreateAPIView):
    """
    Creates the user.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CreateProfile_ByAPI(TemplateView):
    template_name = "myauth/reg_by_api.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Profile creation'
        context['mobile'] = check_on_mobile(self.request)
        return context


class LogView(LoginView):
    template_name = 'myauth/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login'
        context['mobile'] = check_on_mobile(self.request)
        return context

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        messages.error(self.request,
                       'Please enter a correct username and password. Note that both fields may be case-sensitive.')
        return super().form_invalid(form)
