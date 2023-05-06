from django.contrib import admin

from chat.models import *

# Register your models here.
admin.site.register(ChatGroup)
admin.site.register(PersonalChatGroup)
admin.site.register(Message)
admin.site.register(PersonalMessage)

