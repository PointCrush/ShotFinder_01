from django.urls import path
from chat.views import *

urlpatterns = [
    path('private/<str:owner_name>/<str:room_name>', personal_chat_room, name='personal_chat_room'),
    path('project/<str:room_name>', project_chat_room, name='project_chat_room'),
]
