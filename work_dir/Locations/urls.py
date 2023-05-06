from django.contrib import admin
from django.urls import path

from .views import *

urlpatterns = [
    path('all/', AllLocationList.as_view(), name='all_locations'),
    path('my/', my_locations, name='my_locations'),
    path('<int:loc_pk>/', locations_detail, name='locations_detail'),
    path('upload_image_location/<int:loc_pk>/', upload_image_location, name='upload_image_location'),
    path('create/', create_location, name='create_location'),
    path('edit/<int:loc_pk>/', edit_location, name='edit_location'),
    path('delete/<int:loc_pk>/', delete_location, name='delete_location'),

    # path('post/<int:post_id>/', show_ph_post, name='ph_post'),
]
