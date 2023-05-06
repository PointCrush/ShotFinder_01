from django.urls import path
from chat.views import *

urlpatterns = [
    path('private/<str:room_name>/', personal_chat_room, name='personal_chat_room'),
    path('project/<str:room_name>/', project_chat_room, name='project_chat_room'),
    path('list/', my_chat_list, name='my_chat_list'),
    path('is_reading/<int:message_pk>/', is_reading, name='is_reading'),
    path('is_reading_personal_message/<int:message_pk>/', is_reading_personal_message, name='is_reading_personal_message'),
]
