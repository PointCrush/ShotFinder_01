from allauth.account.decorators import verified_email_required
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator

from Project_01.models import ProjectMember
from .models import *


@verified_email_required
# Create your views here.
def list_notification(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')

    paginator = Paginator(notifications, 3)
    page = request.GET.get('page')
    my_objects = paginator.get_page(page)

    context = {
        'my_objects': my_objects,
    }
    return render(request, 'list_notification.html', context)


@verified_email_required
def list_invite(request):
    invite = Invite.objects.filter(whom=request.user).order_by('-created_at')
    lst = []
    if invite:
        for i in invite:
            project_pk = i.project.pk
            model = i.role.content_type.model_class()
            member_pk = ProjectMember.objects.get(content_type=i.role.content_type,
                                                  object_id=model.objects.get(owner=request.user).pk,
                                                  project=Project_01.objects.get(pk=project_pk),
                                                  ).pk
            data_list = [i, project_pk, member_pk]
            lst.append(data_list)
    else:
        project_pk = None
        member_pk = None

    paginator = Paginator(lst, 10)
    page = request.GET.get('page')
    my_objects = paginator.get_page(page)

    context = {
        'my_objects': my_objects,
        'project_pk': project_pk,
        'member_pk': member_pk,
    }
    return render(request, 'list_invite.html', context)


@verified_email_required
def delete_invite(request, invite_pk):
    invite = Invite.objects.get(pk=invite_pk)
    if invite.whom == request.user:
        invite.delete()
    return redirect('list_invite')


def read_notification(request, pk):
    notification = Notification.objects.get(pk=pk)
    notification.delete()
    return HttpResponse(status=200)
