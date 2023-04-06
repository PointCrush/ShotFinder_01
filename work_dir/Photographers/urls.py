from django.contrib import admin
from django.urls import path

from .views import *

urlpatterns = [
    path('', PhotographerPage.as_view(), name='photographers'),
    path('post/<int:post_id>/', show_ph_post, name='ph_post'),
    path('post/<int:post_id>/edit', edit_ph_post, name='edit_ph_post'),
    path('create_ph/', create_ph, name='create_ph'),
    path('delete_photo/<int:photo_id>/', delete_photo, name='ph_delete_photo'),
    path('delete_photos/', delete_photos, name='ph_delete_photos'),
    path('comment/<int:pk>/delete/', ph_comment_delete, name='ph_comment_delete'),
    path('like/<int:pk>/', like_view, name='ph_like_view'),
    path('liked/', liked_ph, name='liked_ph'),
    path('post/<int:pk>/photo_editor/<int:album_pk>', ph_photo_editor, name='ph_photo_editor'),
    path('albums/<int:album_id>/photos/', load_photos, name='ph_load_photos'),
    path('move-photos/', move_photos, name='ph_move-photos'),
    path('album_delete/<int:pk>/<int:album_pk>', ph_album_delete, name='ph_album_delete'),

]
