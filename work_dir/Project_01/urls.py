from django.urls import path

from .views import *

urlpatterns = [
    path('', ProjectsPage.as_view(), name='project_list'),
    path('<int:project_pk>/', project_detail, name='project_detail'),
    path('create_project/', create_project, name='create_project'),
    path('upload_references/<int:project_pk>/', upload_image, name='upload_image_proj'),
    path('give_response/', give_response, name='give_response'),
    path('approve/<int:project_pk>/<int:applicant_pk>/', approve, name='approve'),
    path('remove/<int:project_pk>/<int:member_pk>/', remove_from_project, name='remove_from_project'),
    path('my_projects/', my_projects, name='my_projects'),
    path('edit_project/<int:project_pk>/', edit_project, name='edit_project'),
    path('delete_project/<int:project_pk>/', delete_project, name='delete_project'),
    # path('post/<int:pk>/photo_editor/<int:album_pk>', ph_photo_editor, name='ph_photo_editor'),
    # path('albums/<int:album_id>/photos/', load_photos, name='ph_load_photos'),
    # path('move-photos/', move_photos, name='ph_move-photos'),
    # path('album_delete/<int:pk>/<int:album_pk>', ph_album_delete, name='ph_album_delete'),

]