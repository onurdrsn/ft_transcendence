from django.urls import path
from .views import *

app_name = 'account'

urlpatterns = [
    path('', home_view, name="home"),
    path('account/<user_id>/', account_view, name='account_view'),
    path('account/<user_id>/edit', edit_account_view, name='edit_view'),
    path('search/', profile_search_view, name='search'),
    path('register/', signup, name="register"),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
]
