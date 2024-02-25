from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
import datetime
from django.core.cache import cache
from django.utils.translation import activate
from django.contrib.sessions.middleware import SessionMiddleware


class LanguageMiddleware(SessionMiddleware):
    def process_request(self, request):
        super().process_request(request)
        language = request.POST.get('language')
        if language is not None:
            activate(language)
            request.session['lang'] = language
        elif 'lang' in request.session:
            activate(request.session['lang'])


class ActiveUserMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if request.user.is_authenticated:
            cache.set('seen_%s' % request.user.username, datetime.datetime.now(), settings.USER_LAST_SEEN_TIMEOUT)
