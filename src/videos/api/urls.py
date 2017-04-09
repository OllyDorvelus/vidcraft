__author__ = 'OllyD'
app_name = "videosapi"
from django.conf.urls import url
from .views import VideoModelListAPIView


urlpatterns = [
    #url(r'^$', UserView.as_view(), name='list'),
    url(r'^$', VideoModelListAPIView.as_view(), name='list'),
    #url(r'^(?P<username>[\w.@+-]+)/$', UserDetailAPIView.as_view(), name='user-detailAPI'),
   # url(r'^(?P<pk>\d+)/like/$', FollowToggleAPIView.as_view(), name='follow-toggle'),
]