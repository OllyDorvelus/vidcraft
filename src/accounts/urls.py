__author__ = 'OllyD'

from django.conf.urls import url
from . import views

app_name = 'accounts'

urlpatterns = [

    url(r'^login/$', views.UserLoginFormView.as_view(), name="login"),
    url(r'^register/$', views.UserRegisterFormView.as_view(), name="register"),
    url(r'^$', views.home, name="home"),
    url(r'^logout/$', views.logout_view, name="logout"),
    url(r'^crafters/$', views.ProfileListView.as_view(), name='profile_list'),
    url(r'^manage/$', views.ProfileUpdateView.as_view(), name='profile_update'),
    url(r'^(?P<username>[\w.@+-]+)/$', views.UserDetailView.as_view(), name='profile_detail'),

    #url(r'^(?P<pk>[0-9]+)/manage/$', views.ProfileUpdateView.as_view(), name='profile_update')



]