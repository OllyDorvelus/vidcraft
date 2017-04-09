from django.contrib import admin
from .models import UserProfile
# Register your models here.


class UserProfileAdmin(admin.ModelAdmin):
    # form = TweetModelForm
    list_display = ["id", "first_name", 'last_name', 'user']
    list_filter = ['id']
    class Meta:
        model = UserProfile


admin.site.register(UserProfile, UserProfileAdmin)