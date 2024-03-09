from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from main.views import *
from django.contrib.auth.views import *
from pong.views import fetch_rooms
from django.views.static import serve


urlpatterns = [
	re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
	re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
	path('', include('account.urls', namespace='account')),
	path('admin/', admin.site.urls, name="admin"),
	path('chat/', include('chat.urls', namespace='chat')),
	path('friend/', include('friend.urls', namespace='friend')),
	path('pong/', include('pong.urls', namespace='pong')),
	path('tictac/', include('tictac.urls', namespace='tictac')),
	path('fetch-rooms/', fetch_rooms, name='fetch_rooms'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns += i18n_patterns(
#     *urlpatterns,
#     prefix_default_language=False
# )

urlpatterns += [
    path('i18n/setlang/', set_language, name='set_language'),
]

urlpatterns += [
    path('change/done/', PasswordChangeDoneView.as_view(template_name='password/change_done.html'),
         name='password_change_done'),
    path('change/', PasswordChangeView.as_view(template_name='password/change.html'),
         name='password_change'),
    path('reset/done/', PasswordResetCompleteView.as_view(template_name='password/reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/', PasswordResetMyView.as_view(), name='password_reset'),
    path('complete/', PasswordResetCompleteView.as_view(template_name='password/reset_complete.html'),
         name='password_reset_complete'),
]

handler404 = 'main.views.handler404'

