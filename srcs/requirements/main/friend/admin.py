from django.contrib import admin
from .models import FriendRequest, Friend
from django.utils.translation import gettext_lazy as _


class FriendListAdmin(admin.ModelAdmin):
    list_filter = ['user']
    list_display = ['user']
    search_fields = ['user']
    readonly_fields = ['user']

    class Meta:
        model = Friend


admin.site.register(Friend, FriendListAdmin)


class FriendRequestAdmin(admin.ModelAdmin):
    list_filter = ['sender', 'receiver']
    list_display = ['sender', 'receiver']
    search_fields = ['sender__email', 'sender__username', 'receiver__email', 'receiver__username']

    class Meta:
        model = FriendRequest


admin.site.register(FriendRequest, FriendRequestAdmin)
