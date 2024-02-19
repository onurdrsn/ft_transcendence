from django.core.serializers.python import Serializer
from django.core.cache import cache
import datetime
from django.conf import settings


class LazyAccountEncoder(Serializer):
    def get_dump_object(self, obj):
        dump_object = {}
        dump_object.update({'id': str(obj.id)})
        dump_object.update({'email': str(obj.email)})
        dump_object.update({'username': str(obj.username)})
        dump_object.update({'profile_image': str(obj.profile_image.url)})
        return dump_object


def last_seen(username):
    return cache.get_or_set('seen_%s' % username, datetime.datetime.now(), settings.USER_LAST_SEEN_TIMEOUT)


def online(username):
    if last_seen(username):
        if datetime.datetime.now() > last_seen(username) + datetime.timedelta(
                seconds=settings.USER_ONLINE_TIMEOUT):
            return "Offline"
        else:
            return "Online"
    return "Offline"
