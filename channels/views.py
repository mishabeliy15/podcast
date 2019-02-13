from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView
from .models import Podcast, UserPodcast
from .forms import PodcastModelForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .algorithm import download_audio_Thread, create_podcast
from podcast.views import check_on_mobile


class CreatePodcast(LoginRequiredMixin, CreateView):
    login_url = '/auth/login/'
    redirect_field_name = None
    success_url = '/'
    model = Podcast
    form_class = PodcastModelForm
    template_name = "channels/add_by_id.html"

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        obj = create_podcast(form.data['video_id'])
        if not obj:
            messages.error(self.request, "Video ID isn't valid.")
            return redirect(reverse_lazy("channels:add_by_id"))
        self.object = obj
        user_podcast = UserPodcast(owner=self.request.user, podcast=obj)
        user_podcast.save()
        download_audio_Thread(obj.video_id, obj)
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        podc = Podcast.objects.filter(video_id=form.data['video_id']).first()
        obj = UserPodcast(owner=self.request.user, podcast=podc)
        obj.save()
        return redirect(reverse_lazy("index"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add by id'
        context['mobile'] = check_on_mobile(self.request)
        return context


class UserPodcastListView(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = UserPodcast
    template_name = 'channels/podcast_list.html'
    context_object_name = 'user_podcasts'
    paginate_by = 9

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(owner=self.request.user).order_by("-added_date")
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'My list'
        context['mobile'] = check_on_mobile(self.request)
        return context


class AddPodcastView(LoginRequiredMixin, TemplateView):
    login_url = '/auth/login/'
    template_name = 'channels/add_podcasts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add podcasts'
        if 'search_request' in self.request.GET:
            context['req'] = self.request.GET['search_request']
        context['mobile'] = check_on_mobile(self.request)
        return context

