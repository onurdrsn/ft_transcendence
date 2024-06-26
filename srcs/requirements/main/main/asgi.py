"""Asynchronous Server Gateway Interface"""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
django_asgi_app = get_asgi_application()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from tictac.routing import websocket_urlpatterns as tictac
from chat.routing import websocket_urlpatterns as chat
from pong.routing import websocket_urlpatterns as pong

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                tictac + chat + pong
            )
        ),
    ),
})

