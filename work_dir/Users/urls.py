from django.urls import path

from Users.views import *

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('profile/', profile, name='profile'),
    path('profile/edit', edit_profile, name='edit_profile'),

]
