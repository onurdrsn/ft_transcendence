from django.urls import path
from .consumers import ChatConsumer


websocket_urlpatterns = [
    path('chat/<room_id>/', ChatConsumer.as_asgi()),
]
