from django.shortcuts import render, get_object_or_404
from django.views.generic import View, DetailView, ListView, FormView
from accounts.models import UserProfile
from .models import VideoModel
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your views here.



class VideoDetailView(DetailView):
    model = VideoModel
    qs = VideoModel.objects.all()
    template_name = "videos/video_detail.html"
    context_object_name = "video"


    # def get_object(self):
    #     return get_object_or_404(VideoModel, pk=pk)

class VideoListView(ListView):
    model = VideoModel
    template_name = "videos/video_list.html"
    context_object_name = "videos"

    def get_queryset(self):
        return VideoModel.objects.all()
