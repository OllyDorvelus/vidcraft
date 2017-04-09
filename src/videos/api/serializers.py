__author__ = 'OllyD'
from django.contrib.auth import get_user_model
from accounts.models import UserProfile
from rest_framework import serializers
from videos.models import VideoModel
#from accounts.api.seralizers import UserDisplaySerializer
from django.utils.timesince import timesince
from django.urls import reverse_lazy

User = get_user_model()
class UserDisplaySerializer(serializers.ModelSerializer):
    # follower_count = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'url',

            ]

    def get_url(self, obj):
        return reverse_lazy("accounts:profile_detail", kwargs={"username": obj.username})


class VideoModelSerializer(serializers.ModelSerializer):
   # url = serializers.SerializerMethodField()
    user = UserDisplaySerializer(read_only=True)
    class Meta:
        model = VideoModel
        fields = [
            'user',
            'video',
            'title',
            'liked',
            'description',
        ]


