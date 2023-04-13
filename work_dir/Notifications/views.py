from django.shortcuts import render, redirect
from django.core.paginator import Paginator

from .models import Notification


# Create your views here.
def list_notification(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')

    paginator = Paginator(notifications, 25)
    page = request.GET.get('page')
    my_objects = paginator.get_page(page)

    context = {
        'my_objects': my_objects,
    }
    return render(request, 'list_notification.html', context)
