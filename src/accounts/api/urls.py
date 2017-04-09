__author__ = 'OllyD'

app_name = "accountsapi"
from django.conf.urls import url
from .views import UserProfileListAPIView, UserFollowToggleAPIView, UserDetailAPIView, UserUpdateAPIView


urlpatterns = [
    #url(r'^$', UserView.as_view(), name='list'),
    url(r'^$', UserProfileListAPIView.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/follow/$', UserFollowToggleAPIView.as_view(), name='follow-toggle'),
    url(r'^(?P<pk>\d+)/$', UserDetailAPIView.as_view(), name='user-detailAPI'),
    url(r'^(?P<pk>\d+)/update/$', UserUpdateAPIView.as_view(), name='user-updateAPI'),
    #url(r'^(?P<username>[\w.@+-]+)/$', UserDetailAPIView.as_view(), name='user-detailAPI'),
   # url(r'^(?P<pk>\d+)/like/$', FollowToggleAPIView.as_view(), name='follow-toggle'),
]