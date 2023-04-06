from django.contrib import admin

from Staff.models import *

# Register your models here.
admin.site.register(Staff)
admin.site.register(StuffType)
admin.site.register(CommentStaff)
admin.site.register(AlbumStaff)