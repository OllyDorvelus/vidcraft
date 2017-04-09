# coding=utf-8
from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(
        r'^admin/',
        include(admin.site.urls)
    ),

    url(
        r'',
        include('django_webvideo.urls', namespace='django_webvideo', app_name='django_webvideo')
    ),
)
