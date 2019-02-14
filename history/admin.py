from django.contrib import admin
from .models import Record


@admin.register(Record)
class PodcastAdmin(admin.ModelAdmin):
    list_display = ('user', 'my_podcast','listened', 'dt_start', 'dt_end', 'end_on')
