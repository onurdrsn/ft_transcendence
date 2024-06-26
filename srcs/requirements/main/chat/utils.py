from datetime import datetime
from django.contrib.humanize.templatetags.humanize import naturalday
from django.core.serializers.python import Serializer
from chat.models import PrivateRoom
from chat.constants import *


def find_or_create_private_chat(user1, user2):
    """
        Belirtilen iki kullanıcı arasında özel bir sohbet odası bulur veya oluşturur.
    """
    try:
        chat = PrivateRoom.objects.get(user1=user1, user2=user2)
    except PrivateRoom.DoesNotExist:
        try:
            chat = PrivateRoom.objects.get(user1=user2, user2=user1)
        except PrivateRoom.DoesNotExist:
            chat = PrivateRoom(user1=user1, user2=user2)
            chat.save()
    return chat


def calculate_timestamp(timestamp):
    """
        Belirtilen zaman damgası için okunabilir bir zaman damgası hesaplar.
        1. Today or yesterday:
            - EX: 'today at 10:56 AM'
            - EX: 'yesterday at 5:19 PM'
        2. other:
            - EX: 05/06/2020
            - EX: 12/28/2020
    """
    ts = ""
    # Today or yesterday
    if (naturalday(timestamp) == "today") or (naturalday(timestamp) == "yesterday"):
        str_time = datetime.strftime(timestamp, "%H:%M")
        str_time = str_time.strip("0")
        ts = f"{naturalday(timestamp)} at {str_time}"
    # other days
    else:
        str_time = datetime.strftime(timestamp, "%m/%d/%Y")
        ts = f"{str_time}"
    return str(ts)


class LazyRoomChatMessageEncoder(Serializer):
    """
        RoomChat nesnesini serileştirmek için kullanılır.
    """
    def get_dump_object(self, obj):
        dump_object = {}
        dump_object.update({'msg_type': MESSAGE})
        dump_object.update({'msg_id': str(obj.id)})
        dump_object.update({'user_id': str(obj.user.id)})
        dump_object.update({'username': str(obj.user.username)})
        dump_object.update({'message': str(obj.content)})
        dump_object.update({'profile_image': str(obj.user.profile_image.url)})
        dump_object.update({'natural_timestamp': calculate_timestamp(obj.timestamp)})
        return dump_object
