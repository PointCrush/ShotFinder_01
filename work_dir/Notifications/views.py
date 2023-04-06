from django.shortcuts import render

from .models import Notification


# Create your views here.
def list_notification(request):
    notifications = Notification.objects.filter(user=request.user)
    context = {
        'notifications': notifications,
    }
    return render(request, 'list_notification.html', context)