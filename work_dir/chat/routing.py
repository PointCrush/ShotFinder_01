import channels
from django.urls import path, re_path
from chat import consumers

websocket_urlpatterns = [
    path('ws/chat/<str:room_name>/', consumers.ChatConsumer.as_asgi()),
    path('ws/personal_chat/<str:room_name>/', consumers.PersonalChatConsumer.as_asgi()),
]
