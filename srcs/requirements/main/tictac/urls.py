from django.urls import path
from .views import game_history, tictac, play, update_winner

app_name = 'tictac'

urlpatterns = [
    path('', tictac, name='tictac_create'),
    path('<room_code>', play, name='play'),
    path('history/', game_history, name='game_history'),
    path('update_winner/<room_code>', update_winner, name='update_winner'),
]
