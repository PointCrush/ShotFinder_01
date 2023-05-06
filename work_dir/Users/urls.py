from django.urls import path

from Users.views import *

urlpatterns = [
    # path('register/<str:role>/', register_user, name='register'),
    # path('login/', CustomLoginView.as_view(), name='login'),
    # path('login_redirect/', LoginRedirect.as_view(), name='login_redirect'),
    # path('logout/', logout_user, name='logout'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/profile/edit', edit_profile, name='edit_profile'),
    path('get_changes/', get_changes, name='get_changes'),
    # path('my_calendar/', my_calendar, name='my_calendar'),

]

