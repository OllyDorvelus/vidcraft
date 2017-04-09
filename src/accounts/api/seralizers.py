__author__ = 'OllyD'

from django.contrib.auth import get_user_model
from accounts.models import UserProfile
from rest_framework import serializers
#from videos.api.serializers import VideoModelSerializer
from videos.models import VideoModel
from django.utils.timesince import timesince
from django.urls import reverse_lazy

User = get_user_model()
class VideoModelSerializer(serializers.ModelSerializer):
   # url = serializers.SerializerMethodField()

    class Meta:
        model = VideoModel
        fields = [
            'id',
            'video',
            'title',
            #'liked',
            'description',
        ]

class UserDisplaySerializer(serializers.ModelSerializer):
    # follower_count = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    video_count = serializers.SerializerMethodField()
    videos = serializers.StringRelatedField(many=True)
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'url',
            'videos',
            'video_count',

            ]

    def get_url(self, obj):
        return reverse_lazy("accounts:profile_detail", kwargs={"username": obj.username})

    def get_video_count(self, obj):
        return obj.videos.count()

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserDisplaySerializer(read_only=True)

    is_following = serializers.SerializerMethodField()
    follower_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    following = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='username'
     )
    #date_display = serializers.SerializerMethodField()
    # timesince = serializers.SerializerMethodField()
    class Meta:
        model = UserProfile
        fields = [
            'id',
            'user',
            'following',
            'friends',
            'user_img',
            'first_name',
            'last_name',
            'bio',
            'joindate',
            'is_following',
            'follower_count',
            'following_count',





        ]

    # def get_date_display(self, obj):
    #      return obj.joindate.strftime("%b %d, %Y at %I:%M %p")
    #
    # def get_timesince(self, obj):
    #     return timesince(obj.timestamp) + " ago"
    def get_is_following(self, obj):
        request = self.context.get("request")
        user = request.user
        if user.is_authenticated():
            if obj.user in user.profile.following.all():
                return True
        return False

    def get_follower_count(self, obj):
        return obj.user.followed_by.all().count()

    def get_following_count(self, obj):
        return obj.following.all().count()



