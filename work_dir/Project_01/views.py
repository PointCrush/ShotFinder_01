from allauth.account.decorators import verified_email_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django_filters.views import FilterView
from django.db import transaction

from Models.models import Model
from Notifications.models import Invite
from Photographers.models import Photographer
from Project_01.forms import *
from Project_01.models import *
from Project_01.filters import *
from Staff.models import Staff
from chat.models import ChatGroup


# Create your views here.
class ProjectsPage(FilterView):
    model = Project_01
    template_name = 'list_proj.html'
    filterset_class = ProjectFilter
    extra_context = {
    }

    def get_queryset(self):
        return Project_01.objects.filter(is_published=True).order_by('time_create')


@verified_email_required
def my_projects(request):
    projects_owner = Project_01.objects.filter(owner=request.user)

    model_projects = Model.objects.none()
    staff_projects = Staff.objects.none()
    ph_projects = Photographer.objects.none()
    model_applicant = Model.objects.none()
    staff_applicant = Staff.objects.none()
    ph_applicant = Photographer.objects.none()

    try:
        model_projects = Project_01.objects.filter(members__content_type=ContentType.objects.get_for_model(Model),
                                                   members__object_id=Model.objects.get(owner=request.user).pk,
                                                   members__is_approved=True, members__is_invited=False,
                                                   ).exclude(pk__in=projects_owner.values_list('pk', flat=True))

        model_applicant = Project_01.objects.filter(members__content_type=ContentType.objects.get_for_model(Model),
                                                    members__object_id=Model.objects.get(owner=request.user).pk,
                                                    members__is_approved=False, members__is_invited=False,
                                                    )
    except:
        pass
    try:
        staff_projects = Project_01.objects.filter(members__content_type=ContentType.objects.get_for_model(Staff),
                                                   members__object_id=Staff.objects.get(owner=request.user).pk,
                                                   members__is_approved=True, members__is_invited=False,
                                                   ).exclude(pk__in=projects_owner.values_list('pk', flat=True))

        staff_applicant = Project_01.objects.filter(members__content_type=ContentType.objects.get_for_model(Staff),
                                                    members__object_id=Staff.objects.get(owner=request.user).pk,
                                                    members__is_approved=False, members__is_invited=False,
                                                    )
    except:
        pass
    try:
        ph_projects = Project_01.objects.filter(members__content_type=ContentType.objects.get_for_model(Photographer),
                                                members__object_id=Photographer.objects.get(owner=request.user).pk,
                                                members__is_approved=True, members__is_invited=False,
                                                ).exclude(pk__in=projects_owner.values_list('pk', flat=True))

        ph_applicant = Project_01.objects.filter(members__content_type=ContentType.objects.get_for_model(Photographer),
                                                 members__object_id=Photographer.objects.get(owner=request.user).pk,
                                                 members__is_approved=False, members__is_invited=False,
                                                 )
    except:
        pass
    participant = model_projects | ph_projects | staff_projects
    applicant = model_applicant | ph_applicant | staff_applicant

    new_message_status_list = []
    for project in participant:
        try:
            chat_room = ChatGroup.objects.get(name=str(project.pk))
        except:
            continue
        messages = chat_room.message_set.all()
        new_message_status = 0
        for message in messages:
            message_status = message.statuses.filter(user=request.user).first()
            if message_status:
                if not message_status.is_read:
                    new_message_status = 1
        new_message_status_list.append([project, new_message_status])

    return render(request, 'my_projects.html', {
        'projects_owner': projects_owner,
        'model_projects': model_projects,
        'ph_projects': ph_projects,
        'staff_projects': staff_projects,
        # 'participant': participant,
        'applicant': applicant,
        'new_message_status_list': new_message_status_list,
    })


@verified_email_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectCreateForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    project = form.save(commit=False)
                    project.owner = request.user
                    project.save()
                    form.save_m2m()

                    my_profession = form.cleaned_data['my_profession']
                    model_class = my_profession.content_type.model_class()
                    object_id = model_class.objects.get(owner=request.user).pk

                    member = ProjectMember.objects.create(project=project, content_type=my_profession.content_type,
                                                          object_id=object_id, role=my_profession.name,
                                                          link=my_profession.link,
                                                          is_approved=True)
                return redirect('upload_image_proj', project_pk=project.pk)
            except:
                form = ProjectCreateForm(request.POST)
                error_message = 'отсутсвует выбранная специальность'
                return render(request, 'create_proj.html', {'form': form, 'error_message': error_message})
    else:
        form = ProjectCreateForm()
    return render(request, 'create_proj.html', {'form': form})


@verified_email_required
def upload_image(request, project_pk):
    project = get_object_or_404(Project_01, pk=project_pk)
    if request.method == 'POST':
        upload_form = UploadImageForm(request.POST, request.FILES)
        if upload_form.is_valid():
            images = request.FILES.getlist('images')
            if len(images) > 6:
                upload_form.add_error('images', 'Вы не можете загрузить более 6 изображений.')
            else:
                for image in images:
                    ImageProject01.objects.create(model=project, image=image)
                return redirect('project_detail', project_pk=project.pk)

    else:
        upload_form = UploadImageForm()

    context = {
        'project_pk': project_pk,
        'upload_form': upload_form,
    }
    return render(request, 'references.html', context)


@verified_email_required
def project_detail(request, project_pk):
    user = request.user
    project = get_object_or_404(Project_01, pk=project_pk)
    members = project.members.filter(is_approved=True, is_invited=False)
    members_owner = []
    for member in members:
        members_owner.append(member.member.owner.username)
    applicants = project.members.filter(is_approved=False, is_invited=False)
    invited = project.members.filter(is_approved=True, is_invited=True)
    request.session['list_username_members'] = members_owner

    chat_room, created = ChatGroup.objects.get_or_create(name=project_pk)
    if user not in [chat_room.members]:
        chat_room.members.add(user)
        chat_room.save()
    messages = chat_room.message_set.all()
    new_message_count = 0
    for message in messages:
        message_status = message.statuses.filter(user=user).first()
        if message_status:
            if not message_status.is_read:
                new_message_count += 1
    return render(request, 'detail_project.html',
                  {
                      'project': project,
                      'members': members,
                      'members_owner': members_owner,
                      'applicants': applicants,
                      'invited': invited,
                      'user': user,
                      'new_message_count': new_message_count,
                  })


@verified_email_required
def give_response(request):
    if request.method == 'POST':
        project_id = request.POST.get('project_id')
        profession_id = request.POST.get('profession_id')

        project = get_object_or_404(Project_01, id=project_id)
        profession = get_object_or_404(Professions, id=profession_id)

        model_class = profession.content_type.model_class()
        object = model_class.objects.get(owner=request.user)

        member = ProjectMember(
            project=project,
            content_type=profession.content_type,
            object_id=object.pk,
            role=profession.name,
            link=profession.link,
            is_approved=False
        )
        member.save()

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})


@verified_email_required
def approve(request, project_pk, applicant_pk):
    applicant = get_object_or_404(ProjectMember, pk=applicant_pk)
    applicant.is_approved = True
    applicant.save()
    return redirect('project_detail', project_pk=project_pk)


@verified_email_required
def remove_from_project(request, project_pk, member_pk):
    member = get_object_or_404(ProjectMember, pk=member_pk)
    member.is_approved = False
    member.save()
    return redirect('project_detail', project_pk=project_pk)


@verified_email_required
def accept_invitation(request, project_pk, member_pk):
    member = get_object_or_404(ProjectMember, pk=member_pk)
    member.is_approved = True
    member.is_invited = False
    member.save()
    Invite.objects.get(whom=request.user, project__pk=project_pk).delete()
    return redirect('project_detail', project_pk=project_pk)


@verified_email_required
def edit_project(request, project_pk):
    model = Project_01.objects.get(pk=project_pk)
    if request.user == model.owner:
        if request.method == 'POST':
            form = ProjectCreateForm(request.POST, request.FILES, instance=model)
            if form.is_valid():
                project = form.save(commit=False)
                project.save()
                return redirect('project_detail', project_pk=project_pk)
        else:
            form = ProjectCreateForm(instance=model)
    else:
        return render(request, 'no_entry_edit_project.html')
    return render(request, 'create_proj.html', {'form': form})


@verified_email_required
def edit_references(request, project_pk):
    project = get_object_or_404(Project_01, pk=project_pk)
    if request.method == 'POST':
        upload_form = UploadImageForm(request.POST, request.FILES, instance=project)
        if upload_form.is_valid():
            images = request.FILES.getlist('images')
            if len(images) > 6:
                upload_form.add_error('images', 'Вы не можете загрузить более 6 изображений.')
            else:
                references = project.references.all()
                for reference in references:
                    reference.delete()
                for image in images:
                    ImageProject01.objects.create(model=project, image=image)
                return redirect('project_detail', project_pk=project.pk)

    else:
        upload_form = UploadImageForm()

    context = {
        'project_pk': project_pk,
        'upload_form': upload_form,
    }
    return render(request, 'references.html', context)


@verified_email_required
def delete_project(request, project_pk):
    project = get_object_or_404(Project_01, pk=project_pk)
    if project.owner == request.user:
        project.delete()
    return redirect('my_projects')

# def invite_project(request, project_pk, user_pk):
