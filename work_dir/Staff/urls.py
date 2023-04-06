from django.urls import path

from .views import *

urlpatterns = [
    path('', StaffPage.as_view(), name='staff'),
    path('post/<int:post_id>/', show_post_staff, name='post_staff'),
    path('post/<int:post_id>/edit', edit_post_staff, name='edit_post_staff'),
    path('create/', create_staff, name='create_staff'),
    path('delete_photo/<int:photo_id>/', delete_photo, name='delete_photo_staff'),
    path('delete_photos/', delete_photos, name='delete_photos_staff'),
    path('comment/<int:pk>/delete/', comment_delete_staff, name='comment_delete_staff'),
    path('like/<int:pk>/', like_view, name='like_view_staff'),
    path('liked/', liked_staff, name='liked_staff'),
    path('post/<int:pk>/photo_editor/<int:album_pk>', photo_editor_staff, name='photo_editor_staff'),
    path('albums/<int:album_id>/photos/', load_photos, name='load_photos_staff'),
    path('move-photos/', move_photos, name='move-photos_staff'),
    path('album_delete/<int:pk>/<int:album_pk>', album_delete_staff, name='album_delete_staff'),

]