__author__ = 'OllyD'


from rest_framework import generics, permissions, mixins
from .seralizers import UserDisplaySerializer, User, UserProfileSerializer
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .pagination import StandardResultsPagination
from accounts.models import UserProfile
from rest_framework.response import Response



class UserView(generics.ListAPIView):
    serializer_class = UserDisplaySerializer

    def get_queryset(self, *args, **kwargs):
       return User.objects.all()


class UserProfileListAPIView(generics.ListAPIView):
    serializer_class = UserProfileSerializer
    pagination_class = StandardResultsPagination
    def get_queryset(self, *args, **kwargs):
        # im_following = self.request.user.profile.get_following()
        # qs1 = UserProfile.objects.filter(user__in=im_following).order_by("user.username")
        # qs2 = UserProfile.objects.filter(user=self.request.user)
        qs = UserProfile.objects.all()
        query = self.request.GET.get("q", None)
        if query is not None:
            qs = qs.filter(
               # Q(content__icontains=query) |
                Q(user__username__icontains=query)
            )
        return qs

    def get_seralizer_context(self, *args, **kwargs):
        context = super(UserProfileListAPIView, self).get_seralizer_context(*args, **kwargs)
        context['request'] = self.request
        return context

class UserFollowToggleAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, pk, format=None):
        userProfile_qs = UserProfile.objects.filter(pk=pk)
        message = "Not allowed"
        if request.user.is_authenticated():
            is_following = UserProfile.objects.follow_toggle(request.user, userProfile_qs.first())
            follower_count = UserProfile.objects.follower_count(userProfile_qs.first())
            return Response({'following': is_following, 'follower_count': follower_count})
        return Response({"message": message}, status=400)

class UserDetailAPIView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer

   # def get_queryset(self, *args, **kwargs):
    def get_queryset(self, *args, **kwargs):
        qs = UserProfile.objects.all()
        return qs

class UserUpdateAPIView(generics.UpdateAPIView, mixins.DestroyModelMixin):
    serializer_class = UserProfileSerializer
   # permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self, *args, **kwargs):
        qs = UserProfile.objects.all()
        return qs

    def delete(self, *args, **kwargs):
        return self.destory(self, *args, **kwargs)

