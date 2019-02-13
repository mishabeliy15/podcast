from .models import Podcast
from django.forms import ModelForm

class PodcastModelForm(ModelForm):
    class Meta:
        model = Podcast
        fields = ['video_id']