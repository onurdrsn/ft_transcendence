from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from django.http import JsonResponse
from urllib.parse import urlencode
from itertools import chain
from datetime import datetime
import pytz
from friend.models import Friend
from account.models import User
from chat.models import PrivateRoom, RoomChat
from chat.utils import find_or_create_private_chat
from django.utils.translation import gettext as _


DEBUG = False


def check_authentication(request):
    if not request.user.is_authenticated:
        base_url = reverse('account:login')
        query_string = urlencode({'next': request.path})
        return redirect(f"{base_url}?{query_string}")
    return None


def private_chat_room_view(request, *args, **kwargs):
    authentication_result = check_authentication(request)
    if authentication_result:
        return authentication_result

    room_id = request.GET.get("room_id")
    context = {'m_and_f': get_recent_chatroom_messages(request.user), "BASE_URL": settings.BASE_URL}
    if room_id:
        context["room_id"] = room_id
    context['debug'] = DEBUG
    context['debug_mode'] = settings.DEBUG
    return render(request, "html/room.html", context)


def get_recent_chatroom_messages(user):
    rooms1 = PrivateRoom.objects.filter(user1=user)
    rooms2 = PrivateRoom.objects.filter(user2=user)

    rooms = list(chain(rooms1, rooms2))
    m_and_f = []
    for room in rooms:
        if room.user1 == user:
            friend_user = room.user2
        else:
            friend_user = room.user1

        try:
            friend_list = Friend.objects.get(user=user)
        except Friend.DoesNotExist:
            print(_(f"Friend object not found for user: {user}"))
            continue

        if not friend_list.is_mutual_friend(friend_user):
            chat = find_or_create_private_chat(user, friend_user)
            chat.is_activate = False
            chat.save()
        else:
            try:
                message = RoomChat.objects.filter(room=room, user=friend_user).latest("timestamp")
            except RoomChat.DoesNotExist:
                today = datetime(
                    year=1950,
                    month=1,
                    day=1,
                    hour=1,
                    minute=1,
                    second=1,
                    tzinfo=pytz.UTC
                )
                message = RoomChat(
                    user=friend_user,
                    room=room,
                    timestamp=today,
                    content="",
                )
            m_and_f.append({
                'message': message,
                'friend_user': friend_user
            })

    return sorted(m_and_f, key=lambda x: x['message'].timestamp, reverse=True)


# Ajax call to return a private chatroom or create one if it does not exist
def create_or_return_private_chat(request):
    user1 = request.user
    payload = {}

    if user1.is_authenticated:
        if request.method == "POST":
            user2_id = request.POST.get("user2_id")
            try:
                user2 = User.objects.get(pk=user2_id)
                chat = find_or_create_private_chat(user1, user2)
                payload['response'] = _("Successfully.")
                payload['chatroom_id'] = chat.id
            except User.DoesNotExist:
                payload['response'] = _("Unable to start a chat with that user.")
        else:
            payload['response'] = _("Invalid request method.")
    else:
        payload['response'] = _("You can't start a chat if you are not authenticated.")
    return JsonResponse(payload)
