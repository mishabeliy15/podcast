from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from .models import UserPodcast, Podcast
from .algorithm import create_podcast, download_audio_Thread


class PodcastSerializer(serializers.ModelSerializer):

    class Meta:
        model = Podcast
        fields = '__all__'


class UserPodcastSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(required=False, queryset=User.objects.all())
    podcast = PodcastSerializer(required=False)
    video_id = serializers.CharField(write_only=True)

    class Meta:
        model = UserPodcast
        fields = '__all__'

    def validate_video_id(self, value):
        obj = None
        try:
            obj = Podcast.objects.get(video_id=value)
        except ObjectDoesNotExist:
            obj = create_podcast(value)
            if not obj:
                raise serializers.ValidationError("Video id isn't valid.")
            download_audio_Thread(value, obj)
        return obj

    def create(self, validated_data):
        obj = validated_data['video_id']
        if not obj:
            raise serializers.ValidationError()
        podcast = UserPodcast(owner=validated_data['owner'], podcast=obj)
        podcast.save()
        return podcast
