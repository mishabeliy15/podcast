from django.db import models
from channels.models import UserPodcast


class Record(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    my_podcast = models.ForeignKey(UserPodcast, on_delete=models.CASCADE)
    dt_start = models.DateTimeField(auto_now_add=True)
    dt_end = models.DateTimeField(auto_now=True)
    listened = models.FloatField(default=0)
    end_on = models.IntegerField(default=0)
