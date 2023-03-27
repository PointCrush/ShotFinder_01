from django.contrib import admin

from Photographers.models import *

# Register your models here.
admin.site.register(Photographer)
admin.site.register(ShootingGenre)
admin.site.register(CommentPh)
admin.site.register(AlbumPh)