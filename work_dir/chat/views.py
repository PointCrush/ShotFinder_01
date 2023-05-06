from allauth.account.decorators import verified_email_required
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User

from Project_01.models import Project_01
from .models import ChatGroup, PersonalChatGroup, MessageStatus, Message, PersonalMessage
import re


@verified_email_required
def project_chat_room(request, room_name):
    user = request.user
    project = Project_01.objects.get(pk=room_name)
    room_title = f"{project.name} ({project.city})"
    members_owner = request.session.get('list_username_members', [])
    if user.username in members_owner:
        room, created = ChatGroup.objects.get_or_create(name=room_name)
        if user not in [room.members]:
            room.members.add(user)
            room.save()
        messages = room.message_set.order_by('timestamp')[:]
        message_status_list = []
        for message in messages:
            message_status = message.statuses.filter(user=user).first()
            if message_status:
                if not message_status.is_read:
                    message_status_list.append([message, 1])
                    continue
                else:
                    message_status_list.append([message, 0])
                    continue
            message_status_list.append([message, 0])

        return render(request, 'chat.html', {
            'room_name': room_name,
            'room_title': room_title,
            'messages': messages,
            'message_status_list': message_status_list,
        })
    else:
        return render(request, 'no_entry_project_room_chat.html', {
            'members_owner': members_owner,
        })


@verified_email_required
def personal_chat_room(request, room_name):
    user = request.user
    room_name_split = room_name.split("_")

    whom_list = room_name_split.copy()
    whom_list.remove(str(user.pk))
    whom = whom_list[0]

    whom_user = User.objects.get(pk=int(whom))
    room_title = whom_user.first_name + ' ' + whom_user.last_name

    if str(user.pk) in room_name_split:
        room, created = PersonalChatGroup.objects.get_or_create(name=room_name)
        if created:
            room.members.add(user, whom_user)
            room.save()
        messages = room.personalmessage_set.order_by('timestamp')[:]
        # if messages:
        #     for message in messages:
        #         if message.new and message.author != user:
        #             message.new = False
        #             message.save()
        return render(request, 'personal_chat.html', {
            'room_name': room_name,
            'room_title': room_title,
            'messages': messages,
            'room': room,
            'whom': whom,
        })
    else:
        return render(request, 'no_entry.html')


@verified_email_required
def my_chat_list(request):
    user = request.user
    room_list = user.personal_chat_group.all()
    room_new_messages = []
    for room in room_list:
        new_message_count = room.personalmessage_set.filter(new=True).exclude(author=user).count()
        name_parts = room.name.split('_')
        name_parts.remove(str(user.pk))
        whom_pk = int(name_parts[0])
        whom_user = User.objects.get(pk=whom_pk)
        whom_name = whom_user.first_name + ' ' + whom_user.last_name
        room_new_messages.append([room, new_message_count, whom_name])
    return render(request, 'chat/templates/chat_list.html', {'room_new_messages': room_new_messages})


def is_reading(request, message_pk):
    user = request.user
    message = Message.objects.get(pk=message_pk)
    message_status = message.statuses.filter(user=user).first()
    if not message_status.is_read:
        message_status.is_read = True
        message_status.save()

    return HttpResponse(status=200)


def is_reading_personal_message(request, message_pk):
    message = PersonalMessage.objects.get(pk=message_pk)
    message.new = False
    message.save()
    return HttpResponse(status=200)
