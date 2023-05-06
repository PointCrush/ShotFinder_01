import json

from allauth.account.decorators import verified_email_required
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django_filters.views import FilterView

from .filters import *
from .forms import *
from .models import *


# Create your views here.


class AllStudioList(FilterView):
    model = Studio
    template_name = 'studios_list.html'
    filterset_class = StudioFilter
    extra_context = {
    }


@verified_email_required
def my_studios(request):
    studios = Studio.objects.filter(owner=request.user)
    return render(request, 'my_studio.html', {'studios': studios})


@verified_email_required
def studio_detail(request, studio_pk):
    studio = Studio.objects.get(pk=studio_pk)
    context = {
        'studio': studio,
    }
    return render(request, 'studio_detail.html', context)


@verified_email_required
def create_studio(request):
    if request.method == 'POST':
        create_form = StudioCreationForm(request.POST, request.FILES)
        if create_form.is_valid():
            studio = create_form.save(commit=False)
            studio.owner = request.user
            studio.save()
            hs, create = HaveStudio.objects.get_or_create(user=request.user)
            return redirect('upload_image_studio', studio_pk=studio.pk)
    else:
        create_form = StudioCreationForm()
    context = {
        'create_form': create_form,
    }
    return render(request, 'create_studio.html', context)


@verified_email_required
def upload_image_studio(request, studio_pk):
    studio = Studio.objects.get(pk=studio_pk)
    if request.method == 'POST':
        upload_form = UploadImageForm(request.POST, request.FILES)
        if upload_form.is_valid():
            images = request.FILES.getlist('images')
            for image in images:
                StudioImage.objects.create(studio=studio,
                                           image=image)
            return redirect('studio_detail', studio_pk=studio_pk)
    else:
        upload_form = UploadImageForm()
    context = {
        'upload_form': upload_form,
    }
    return render(request, 'Locations/template/upload_image_form.html', context)


@verified_email_required
def edit_studio(request, studio_pk):
    model = Studio.objects.get(pk=studio_pk)
    if model.owner == request.user:
        if request.method == 'POST':
            form = StudioCreationForm(request.POST, request.FILES, instance=model)
            if form.is_valid():
                form.save()
                return redirect('studio_detail', studio_pk=studio_pk)
        else:
            form = StudioCreationForm(instance=model)
        return render(request, 'Photographers/templates/edit_ph.html', {'form': form})
    else:
        return render(request, 'data_dir/template/access_error.html')


@verified_email_required
def delete_studio(request, studio_pk):
    studio = Studio.objects.get(pk=studio_pk)
    if request.user == studio.owner:
        studio.delete()
        return redirect('my_studios')
    else:
        return render('data_dir/template/access_error.html')


def studio_photo_editor(request, studio_pk):
    studio = get_object_or_404(Studio, pk=studio_pk)

    # Обработка загрузки фотографий
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            images = request.FILES.getlist('images')
            for image in images:
                StudioImage.objects.create(studio=studio,
                                       image=image)
            return redirect('studio_photo_editor', studio_pk=studio_pk)
    else:
        upload_form = UploadImageForm()

    context = {
        'studio': studio,
        'upload_form': upload_form,
    }
    return render(request, 'studio-photo-editor.html', context)


@require_POST
def delete_photos(request):
    if request.method == 'POST':
        photo_ids = json.loads(request.body)
        for photo_id in photo_ids:
            photo = get_object_or_404(StudioImage, pk=photo_id)
            photo.delete()
        return HttpResponse(status=200)
    return HttpResponseBadRequest()
