from . import views
from django.utils.translation import gettext as _
from django.urls import path

app_name = 'pong'

urlpatterns = [
	path('', views.home, name="home"),
	path("game_history/", views.game_history, name='history'),
	path('tournament/', views.tournament, name='tournament'),
	path('update_winner/<room_name>', views.update, name='update'),
	path("<room_name>/", views.room, name='room'),
	path('ai', views.ai, name='ai'),
	path('offline', views.offline, name='offline'),
]
