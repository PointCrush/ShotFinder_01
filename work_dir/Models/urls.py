from django.urls import path, include

from .views import *

urlpatterns = [
    path('', ModelsPage.as_view(), name='models'),
    path('post/<int:post_id>/', show_model_post, name='model_post'),
    path('edit_post/<int:post_id>/', edit_model_post, name='edit_model_post'),
    path('create_model/', create_model, name='create_model'),
    path('delete-photo/<int:photo_id>/', delete_photo, name='delete_photo'),
    path('delete_photos/', delete_photos, name='delete_photos'),
    path('comment/<int:pk>/delete/', comment_delete, name='comment_delete'),
    path('like/<int:pk>/', like_view, name='like_view'),
    path('liked/', liked_models, name='liked_models'),
    path('post/<int:pk>/photo_editor/<int:album_pk>', photo_editor, name='photo_editor'),
    path('albums/<int:album_id>/photos/', load_photos, name='load_photos'),
    path('move-photos/', move_photos, name='move-photos'),
    path('album_delete/<int:pk>/<int:album_pk>', album_delete, name='album_delete'),

]
