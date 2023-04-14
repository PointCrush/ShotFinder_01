from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import ChatGroup
import re


@login_required
def project_chat_room(request, room_name):
    user = request.user
    members_owner = request.session.get('list_username_members', [])
    if user.username in members_owner:
        room, created = ChatGroup.objects.get_or_create(name=room_name)
        messages = room.message_set.order_by('timestamp')[:]
        return render(request, 'chat.html', {
            'room_name': room_name,
            'messages': messages,
        })
    else:
        return render(request, 'project_room.html', {
            'members_owner': members_owner,
        })


@login_required
def personal_chat_room(request, owner_name, room_name):
    user = request.user
    room_name_list = room_name.split("_")
    if user.username in room_name_list and owner_name in room_name_list:
        room, created = ChatGroup.objects.get_or_create(name=room_name)
        messages = room.message_set.order_by('timestamp')[:]
        return render(request, 'chat.html', {
            'room_name': room_name,
            'messages': messages,
        })
    else:
        return render(request, 'no_entry.html')
