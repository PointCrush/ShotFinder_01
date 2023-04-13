from django.shortcuts import render
from .models import ChatGroup


def chat_room(request, room_name):
    room, created = ChatGroup.objects.get_or_create(name=room_name)
    messages = room.message_set.order_by('timestamp')[:50]
    return render(request, 'chat.html', {
        'room_name': room_name,
        'messages': messages,
    })
