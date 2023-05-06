from django.contrib import admin
from django.urls import path

from .views import *

urlpatterns = [
    path('all/', AllStudioList.as_view(), name='list_studios'),
    path('my/', my_studios, name='my_studios'),
    path('<int:studio_pk>/', studio_detail, name='studio_detail'),
    path('upload_image_studio/<int:studio_pk>/', upload_image_studio, name='upload_image_studio'),
    path('create/', create_studio, name='create_studio'),
    path('edit/<int:studio_pk>/', edit_studio, name='edit_studio'),
    path('delete/<int:studio_pk>/', delete_studio, name='delete_studio'),
    path('photo_editor/<int:studio_pk>/', studio_photo_editor, name='studio_photo_editor'),
    path('delete_photos/', delete_photos, name='studio_delete_photos'),

    # path('post/<int:post_id>/', show_ph_post, name='ph_post'),
]
