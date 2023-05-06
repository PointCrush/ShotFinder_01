import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from Project_01.models import Project_01
from chat.models import ChatGroup, Message, PersonalMessage, PersonalChatGroup, MessageStatus


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Присоединение к группе
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Отсоединение от группы
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Получение сообщений от WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        if not message:
            message = ' '
        user = self.scope['user']

        # Создание объекта сообщения в базе данных
        room = await sync_to_async(lambda: ChatGroup.objects.get(name=self.room_name))()
        message_object = await sync_to_async(lambda: Message.objects.create(content=message, author=user, chat_group=room))()

        members = await sync_to_async(lambda: list(room.members.all()))()

        for member in members:
            if member != user:
                await sync_to_async(lambda: MessageStatus.objects.create(message=message_object, user=member))()

        # Отправка сообщения всем участникам чата
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': f"{user}: {message}"
            }
        )

    # Получение сообщения от группы
    async def chat_message(self, event):
        message = event['message']

        # Отправка сообщения клиенту WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))


class PersonalChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Присоединение к группе
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Отсоединение от группы
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Получение сообщений от WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = self.scope['user']

        # Создание объекта сообщения в базе данных
        room = await sync_to_async(lambda: PersonalChatGroup.objects.get(name=self.room_name))()
        await sync_to_async(lambda: PersonalMessage.objects.create(content=message, author=user, chat_group=room))()

        # Отправка сообщения всем участникам чата
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': f"{user}: {message}"
            }
        )

    # Получение сообщения от группы
    async def chat_message(self, event):
        message = event['message']

        # Отправка сообщения клиенту WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
