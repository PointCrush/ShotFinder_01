from django.urls import path

from .views import *

urlpatterns = [
    path('my_notifications/', list_notification, name='list_notification'),

]