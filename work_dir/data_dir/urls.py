"""data_dir URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include

from Users.views import home
from data_dir import settings

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('home/', home, name='home'),

    path('', include('Users.urls')),
    path('models/', include('Models.urls')),
    path('photographers/', include('Photographers.urls')),
    path('staff/', include('Staff.urls')),
    path('projects/', include('Project_01.urls')),
    path('calendar/', include('Calendar.urls')),
    path('notifications/', include('Notifications.urls')),
    path('chat/', include('chat.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
