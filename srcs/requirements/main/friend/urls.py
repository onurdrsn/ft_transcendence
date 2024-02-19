from django.urls import path
from .views import *

app_name = 'friend'

urlpatterns = [
    path('block_user', block_user_view, name='block_user'),
    path('cancel_friend/', cancel_friend, name='cancel_friend'),
    path('friend_remove', remove_friend_request, name='remove_friend_request'),
    path('friend_request', index, name='friend_request'),
    path('unblock_user', unblock_user_view, name='unblock_user'),
    path('accept_friend/<friend_request_id>', accept_friend_request, name='accept_friend_request'),
    path('decline_user/<friend_request_id>', decline_friend, name='decline_friend'),
    path('friend_request/<user_id>', friend_request_view, name='friend_requests'),
    path('list/<user_id>', friends_list_view, name='friends_list_view'),
    path('list/', default_index, name='friends_list_index'),
]
