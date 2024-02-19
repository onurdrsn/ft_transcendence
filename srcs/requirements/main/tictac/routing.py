from django.urls import path
from .consumers import GameConsumer

websocket_urlpatterns = [
    # re_path(r'^ws/game/(?P<room_code>)', GameConsumer.as_asgi()),
    path('ws/game/<room_code>', GameConsumer.as_asgi()),
]
