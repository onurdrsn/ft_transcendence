from django.http import HttpResponse
import json
from django.shortcuts import redirect, render
from account.models import User
from .models import FriendRequest, Friend
from django.utils.translation import gettext_lazy as _


def default_index(request, *args, **kwargs):
    if request.user.is_authenticated:
        return render(request, "friend_list_2.html")
    else:
        redirect("login")


def friend_request_view(request, *args, **kwargs):
    context = {}
    if request.user.is_authenticated:
        account = User.objects.get(pk=kwargs['user_id'])
        if account == request.user:
            context['friend_requests'] = FriendRequest.objects.filter(receiver=account, is_active=True)
        else:
            return HttpResponse(_("U can't view another users friend requests."))
    else:
        redirect("login")
    return render(request, "friend_request.html", context)


def index(request, *args, **kwargs):
    user = request.user
    payload = {}
    if request.method == 'POST' and user.is_authenticated:
        user_id = json.loads(request.body)['receiver_user_id']
        if user_id:
            receiver = User.objects.get(pk=user_id)
            try:
                # get any friend request (active and no-active)
                friend_requests = FriendRequest.objects.filter(sender=user, receiver=receiver)
                # find if any of them are active
                try:
                    for request in friend_requests:
                        if request.is_active:
                            raise Exception(str(_("U already sent them a friend request.")))
                    # if no are activate, then create a new friend request
                    FriendRequest(sender=user, receiver=receiver).save()
                    payload['response'] = str(_("Friend request sent."))
                except Exception as e:
                    payload['response'] = str(e)
            except FriendRequest.DoesNotExist:
                # there are no friend requests so create one.
                FriendRequest(sender=user, receiver=receiver).save()
                payload['response'] = str(_("Friend request sent."))

            if payload['response'] == 'None':
                payload['response'] = str(_("Something went wrong."))
        else:
            payload['response'] = str(_("Unable to send a friend request."))
    else:
        payload['response'] = str(_("U must be authenticated to send a friend request."))
    return HttpResponse(json.dumps(payload), content_type="application/json")


def accept_friend_request(request, *args, **kwargs):
    payload = {}
    if request.method == 'GET' and request.user.is_authenticated:
        if kwargs['friend_request_id']:
            friend_req = FriendRequest.objects.get(pk=kwargs['friend_request_id'])
            # confirm that is the correct request
            if friend_req.receiver == request.user:
                if friend_req:
                    # found the request. not accept it
                    friend_req.accept()
                    payload['response'] = str(_("Friend request accepted."))
                else:
                    payload['response'] = str(_("Something went wrong."))
            else:
                payload['response'] = str(_("That is not your friend request."))
        else:
            payload['response'] = str(_("Unable to send a friend request."))
    else:
        payload['response'] = str(_("U must be authenticated to send a friend request."))
    return HttpResponse(json.dumps(payload), content_type="application/json")


def remove_friend_request(request, *args, **kwargs):
    user = request.user
    payload = {}
    if request.method == 'POST' and user.is_authenticated:
        user_id = json.loads(request.body)['receiver_user_id']
        if user_id:
            try:
                Friend.objects.get(user=user).unfriend(User.objects.get(pk=user_id))
                payload['response'] = str(_("Successfully removed friend."))
            except Exception as e:
                payload['response'] = str(_("Something went wrong {}").format(str(e)))
        else:
            payload['response'] = str(_("There was an error. Unable to remove that friend."))
    else:
        payload['response'] = str(_("U must be authenticated to remove a friend."))
    return HttpResponse(json.dumps(payload), content_type="application/json")


def block_user_view(request, *args, **kwargs):
    user = request.user
    payload = {}
    if request.method == 'POST' and user.is_authenticated:
        user_id_to_block = json.loads(request.body)['receiver_user_id']
        if user_id_to_block:
            try:
                Friend.objects.get(user=user).block_user(User.objects.get(pk=user_id_to_block))
                payload['response'] = str(_("Successfully blocked user."))
            except Exception as e:
                payload['response'] = str(_("Something went wrong {}").format(str(e)))
        else:
            payload['response'] = str(_("There was an error. Unable to block that user."))
    else:
        payload['response'] = str(_("You must be authenticated to block a user."))
    return HttpResponse(json.dumps(payload), content_type="application/json")


def unblock_user_view(request, *args, **kwargs):
    user = request.user
    payload = {}
    if request.method == 'POST' and user.is_authenticated:
        user_id_to_unblock = json.loads(request.body)['receiver_user_id']
        if user_id_to_unblock:
            try:
                Friend.objects.get(user=user).unblock_user(User.objects.get(pk=user_id_to_unblock))
                payload['response'] = str(_("Successfully unblocked user."))
            except Exception as e:
                payload['response'] = str(_("Something went wrong {}").format(str(e)))
        else:
            payload['response'] = str(_("There was an error. Unable to unblock that user."))
    else:
        payload['response'] = str(_("You must be authenticated to unblock a user."))
    return HttpResponse(json.dumps(payload), content_type="application/json")


def decline_friend(request, *args, **kwargs):
    user = request.user
    payload = {}
    if request.method == 'GET' and user.is_authenticated:
        friend_request_id = kwargs['friend_request_id']
        if friend_request_id:
            friend_request = FriendRequest.objects.get(pk=friend_request_id)
            # confirm that it is correct
            if friend_request.receiver == user:
                if friend_request:
                    friend_request.decline()
                    payload['response'] = str(_("Friend request declined."))
                else:
                    payload['response'] = str(_("Something went wrong."))
            else:
                payload['response'] = str(_("That is not your friend request to decline."))
        else:
            payload['response'] = str(_("Unable to decline friend request."))
    else:
        payload['response'] = str(_("U must be authenticated."))
    return HttpResponse(json.dumps(payload), content_type="application/json")


def cancel_friend(request, *args, **kwargs):
    user = request.user
    friend_requests = None
    payload = {}
    if request.method == "POST" and user.is_authenticated:
        user_id = json.loads(request.body)['receiver_user_id']
        if user_id:
            receiver = User.objects.get(pk=user_id)
            try:
                friend_requests = FriendRequest.objects.filter(sender=user, receiver=receiver, is_active=True)
            except FriendRequest.DoesNotExist:
                payload['response'] = str(_("Nothing to cancel. Friend request does not exist."))
            # There should only ever be ONE active friend request at any given time. Cancel them all just in case.
            if len(friend_requests) > 1:
                for request in friend_requests:
                    request.cancel()
                payload['response'] = str(_("Friend request canceled."))
            else:
                # found the request. Now cancel it
                friend_requests.first().cancel()
                payload['response'] = str(_("Friend request canceled."))
        else:
            payload['response'] = str(_("Unable to cancel that friend request."))
    else:
        # should never happen
        payload['response'] = str(_("You must be authenticated to cancel a friend request."))
    return HttpResponse(json.dumps(payload), content_type="application/json")


def friends_list_view(request, *args, **kwargs):
    context = {}
    user = request.user
    if user.is_authenticated:
        user_id = kwargs.get("user_id")
        if user_id:
            try:
                this_user = User.objects.get(pk=user_id)
                context['this_user'] = this_user
            except User.DoesNotExist:
                return HttpResponse(_("That user does not exist."))
            try:
                friend_list = Friend.objects.get(user=this_user)
            except Friend.DoesNotExist:
                return HttpResponse(_("Could not find a friends list for {}").format(this_user.username))

            # Must be friends to view a friends list
            if user != this_user:
                if user not in friend_list.friends.all():
                    return HttpResponse(_("You must be friends to view their friends list."))
            friends = []
            # get the authenticated users friend list
            auth_user_friend_list = Friend.objects.get(user=user)
            for friend in friend_list.friends.all():
                friends.append((friend, auth_user_friend_list.is_mutual_friend(friend)))
            context['friends'] = friends
        else:
            redirect('index')
    else:
        return HttpResponse(_("You must be friends to view their friends list."))
    return render(request, "friend_list.html", context)
