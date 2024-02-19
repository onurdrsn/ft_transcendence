from django.db import models
from django.conf import settings
from django.utils import timezone


class Friend(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user')
    friends = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="friends")
    blocked_users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="blocked_by")

    def __str__(self):
        return self.user.username

    def add_friend(self, friend):
        if friend not in self.friends.all():
            self.friends.add(friend)

    def remove_friend(self, friend):
        if friend in self.friends.all():
            self.friends.remove(friend)

    def unfriend(self, friend):
        self.remove_friend(friend)
        friends_list = Friend.objects.get(user=friend)
        friends_list.remove_friend(self.user)

    def is_mutual_friend(self, friend):
        return friend in self.friends.all()

    def block_user(self, user):
        if user not in self.blocked_users.all():
            friend_request = FriendRequest.objects.filter(sender=self.user, receiver=user, is_active=True).first()
            if friend_request:
                friend_request.cancel()
            self.blocked_users.add(user)
            self.unfriend(user)

    def unblock_user(self, user):
        if user in self.blocked_users.all():
            self.blocked_users.remove(user)
            Friend.objects.get(user=user).blocked_users.remove(self.user)

    def is_blocked(self, user):
        return user in self.blocked_users.all()


class FriendRequest(models.Model):
    """
    1. sender
    2. receiver
    """
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='receiver')
    is_active = models.BooleanField(blank=True, null=False, default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.username

    def accept(self):
        receiver_friend_list = Friend.objects.get(user=self.receiver)
        sender_friend_list = None
        if receiver_friend_list:
            if not receiver_friend_list.is_blocked(self.sender):
                receiver_friend_list.add_friend(self.sender)
                sender_friend_list = Friend.objects.get(user=self.sender)
            if sender_friend_list:
                if not sender_friend_list.is_blocked(self.receiver):
                    sender_friend_list.add_friend(self.receiver)
                    self.is_active = False
                    self.save()

    def decline(self):
        self.is_active = False
        self.save()

    def cancel(self):
        self.is_active = False
        self.save()
