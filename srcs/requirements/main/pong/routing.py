from django.urls import path
from .consumer import GameConsumer, AnasayfaConsumer


websocket_urlpatterns = [
	path('ws/anasayfa/', AnasayfaConsumer.as_asgi()),
	path('ws/pong/<room_name>', GameConsumer.as_asgi()),
]
