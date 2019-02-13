from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(LoginRequiredMixin, TemplateView):
    login_url = '/startpage/'
    template_name = 'main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Get it now!'
        context['mobile'] = check_on_mobile(self.request)
        return context

    def get(self, request, *args, **kwargs):
        return redirect('channels:podcast_list')


class StartPageView(TemplateView):
    template_name = 'startpage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Get it now!'
        context['mobile'] = check_on_mobile(self.request)
        return context


@login_required
def redirect_index_view(request):
    return redirect('startpage')


def check_on_mobile(request):
    s = request.META['HTTP_USER_AGENT'].lower()
    for i in ['android', 'iphone', 'mobile']:
        if i in s:
            return True
    return False
