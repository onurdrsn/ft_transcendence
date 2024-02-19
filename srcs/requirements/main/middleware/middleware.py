from django.utils import translation
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from asgiref.sync import sync_to_async
import datetime
from django.core.cache import cache


class LanguageMiddleware(MiddlewareMixin):

    async def __call__(self, request):
        language = request.POST.get('language')
        if language is not None:
            translation.activate(language)
            request.language = language
            await sync_to_async(request.session.__setitem__)('lang', language)
        elif await sync_to_async(request.session.__contains__)('lang'):
            translation.activate(await sync_to_async(request.session.__getitem__)('lang'))
        response = await self.get_response(request)
        if await sync_to_async(request.session.__contains__)('lang'):
            response.set_cookie('lang', await sync_to_async(request.session.__getitem__)('lang'))
        return response


class ActiveUserMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if request.user.is_authenticated:
            cache.set('seen_%s' % request.user.username, datetime.datetime.now(), settings.USER_LAST_SEEN_TIMEOUT)
