from django.urls import path
from .views import *

app_name = 'chat'

urlpatterns = [
    path('', private_chat_room_view, name='private_chat_room'),
    path('create/', create_or_return_private_chat, name='create_or_return_private_chat'),
]
