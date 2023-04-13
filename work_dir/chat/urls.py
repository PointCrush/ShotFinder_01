from django.urls import path
from chat.views import *

urlpatterns = [
    path('<str:room_name>', chat_room, name='chat_room'),
]
