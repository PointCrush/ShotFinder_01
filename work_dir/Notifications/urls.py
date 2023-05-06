from django.urls import path

from .views import *

urlpatterns = [
    path('my_notifications/', list_notification, name='list_notification'),
    path('my_invite/', list_invite, name='list_invite'),
    path('my_invite/delete/<int:invite_pk>/', delete_invite, name='delete_invite'),
    path('read_notification/<int:pk>/', read_notification, name='read_notification'),

]