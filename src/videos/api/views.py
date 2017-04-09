__author__ = 'OllyD'


from rest_framework import generics, permissions, mixins
#from .seralizers import UserDisplaySerializer, User, UserProfileSerializer
from .serializers import VideoModelSerializer
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .pagination import StandardResultsPagination
from accounts.models import UserProfile
from videos.models import VideoModel
from rest_framework.response import Response



class VideoModelListAPIView(generics.ListAPIView):
    serializer_class = VideoModelSerializer
    pagination_class = StandardResultsPagination
    def get_queryset(self, *args, **kwargs):
        # im_following = self.request.user.profile.get_following()
        # qs1 = UserProfile.objects.filter(user__in=im_following).order_by("user.username")
        # qs2 = UserProfile.objects.filter(user=self.request.user)
        qs = VideoModel.objects.all()
        query = self.request.GET.get("q", None)
        if query is not None:
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(user__username__icontains=query)
            )
        return qs

    def get_seralizer_context(self, *args, **kwargs):
        context = super(VideoModelSerializer, self).get_seralizer_context(*args, **kwargs)
        context['request'] = self.request
        return context