from django.contrib import admin
from .models import Podcast, UserPodcast


@admin.register(Podcast)
class PodcastAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration', 'processed', 'listened', 'counts_add', 'downloads', 'channel_name', 'created_data')


@admin.register(UserPodcast)
class UserPodcastAdmin(admin.ModelAdmin):
    list_display = ('podcast', 'owner', 'processed', 'duration', 'duration_listened', 'downloads', 'watched_date', 'added_date')

    def duration(self, obj):
        return obj.podcast.duration

    def processed(self, o):
        return o.podcast.processed

    duration.admin_order_field = 'podcast__duration'
    processed.admin_order_field = 'podcast__processed'
