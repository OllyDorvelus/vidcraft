__author__ = 'OllyD'
from django.conf.urls import url
from . import views

app_name = 'videos'


urlpatterns = [
            url(r'^videos/browse/$', views.VideoListView.as_view(), name="video_list"),
            url(r'^video/(?P<pk>\d+)/$', views.VideoDetailView.as_view(), name="video_detail"),

        ]