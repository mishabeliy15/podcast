from django.db import models
from django.utils import timezone


class Podcast(models.Model):
    name = models.CharField(max_length=256)
    video_id = models.CharField(max_length=128, unique=True)
    duration = models.IntegerField()
    channel_id = models.CharField(max_length=128)
    channel_name = models.CharField(max_length=256)
    created_data = models.DateTimeField(default=timezone.now)
    thumbnails_url = models.CharField(max_length=256, null=True, verbose_name="Image URL")
    processed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def counts_add(self):
        return UserPodcast.objects.filter(podcast=self).count()

    def listened(self):
        return sum(o.duration_listened for o in UserPodcast.objects.filter(podcast=self))

    def downloads(self):
        return sum(o.downloads for o in UserPodcast.objects.filter(podcast=self))


class UserPodcast(models.Model):
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE)
    added_date = models.DateTimeField(default=timezone.now)
    watched_date = models.DateTimeField(blank=True, null=True)
    duration_listened = models.IntegerField(default=0)
    downloads = models.IntegerField(default=0)

    def __str__(self):
        return self.podcast.name

    def watched(self):
        self.watched_date = timezone.now()
        self.save()
        return self

    def listened_n(self, n=15):
        self.duration_listened += round(n)
        self.save()
        return self

    def downloaded_inc(self):
        self.downloads += 1
        self.save()
        return self
