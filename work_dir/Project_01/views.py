from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django_filters.views import FilterView

from Project_01.forms import *
from Project_01.models import *
from Project_01.filters import *


# Create your views here.
class ProjectsPage(FilterView):
    model = Project_01
    template_name = 'list_proj.html'
    filterset_class = ProjectFilter
    extra_context = {
    }

    def get_queryset(self):
        return Project_01.objects.filter(is_published=True).order_by('time_create')


def my_projects(request):
    projects = Project_01.objects.filter(owner=request.user)

    return render(request, 'my_projects.html', {'projects': projects})


@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectCreateForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            form.save_m2m()

            my_profession = form.cleaned_data['my_profession']
            model_class = my_profession.content_type.model_class()
            object_id = model_class.objects.get(owner=request.user).pk

            member = ProjectMember.objects.create(project=project, content_type=my_profession.content_type,
                                                  object_id=object_id, role=my_profession.name, link=my_profession.link,
                                                  is_approved=True)
            return redirect('upload_image_proj', project_pk=project.pk)
    else:
        form = ProjectCreateForm()
    return render(request, 'create_proj.html', {'form': form})


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


def project_detail(request, project_pk):
    project = get_object_or_404(Project_01, pk=project_pk)
    members = project.members.filter(is_approved=True)
    applicants = project.members.filter(is_approved=False)
    return render(request, 'detail_proj.html', {'project': project, 'members': members, 'applicants': applicants})


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


def approve(request, project_pk, applicant_pk):
    applicant = get_object_or_404(ProjectMember, pk=applicant_pk)
    applicant.is_approved = True
    applicant.save()
    return redirect('project_detail', project_pk=project_pk)


def remove_from_project(request, project_pk, member_pk):
    member = get_object_or_404(ProjectMember, pk=member_pk)
    member.is_approved = False
    member.save()
    return redirect('project_detail', project_pk=project_pk)
