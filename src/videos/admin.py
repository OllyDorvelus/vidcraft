from django.contrib import admin
from .models import VideoModel
# Register your models here.


class VideoModelAdmin(admin.ModelAdmin):
    # form = TweetModelForm
    list_display = ["id", "title", 'description', 'user']
    list_filter = ['id']
    class Meta:
        model = VideoModel


admin.site.register(VideoModel, VideoModelAdmin)