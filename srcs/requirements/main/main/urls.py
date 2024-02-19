from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from main.views import *
from django.contrib.auth.views import *

urlpatterns = [
    path('', include('account.urls', namespace='account')),
    path('admin/', admin.site.urls, name="admin"),
    path('chat/', include('chat.urls', namespace='chat')),
    path('friend/', include('friend.urls', namespace='friend')),
    path('tictac/', include('tictac.urls', namespace='tictac')),
    path('changelog', changelog, name='changelog'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

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
