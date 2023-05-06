from django.db import models
from django.contrib.auth.models import User


class ChatGroup(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(User, related_name='chat_group')

    def __str__(self):
        return self.name


class PersonalChatGroup(models.Model):
    name = models.CharField(max_length=255)
    owner_name = models.CharField(max_length=255, default='owner_name')
    view_name = models.CharField(max_length=255, default='view_name')
    members = models.ManyToManyField(User, related_name='personal_chat_group')

    def __str__(self):
        return self.name


class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    chat_group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    new = models.BooleanField(default=True)

    class Meta:
        ordering = ('timestamp',)

    def __str__(self):
        r = self.author.username + self.content
        return r


class MessageStatus(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='statuses')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_statuses')
    is_read = models.BooleanField(default=False)

    class Meta:
        unique_together = ('message', 'user')


class PersonalMessage(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    chat_group = models.ForeignKey(PersonalChatGroup, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    new = models.BooleanField(default=True)

    class Meta:
        ordering = ('timestamp',)

    def __str__(self):
        r = self.author.username + self.content
        return r
