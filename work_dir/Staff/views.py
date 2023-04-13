import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django_filters.views import FilterView
from django.contrib import messages

from Notifications.models import Notification
from Staff.filters import *
from Staff.forms import *
from Staff.models import *

# Create your views here.
class StaffPage(FilterView):
    model = Staff
    template_name = 'content_staff.html'
    filterset_class = StaffFilter
    extra_context = {
        'title': 'Стилисты',
        'object': 'стилиста',
        'create': 'create_staff',
        'post': 'post_staff',
    }

    def get_queryset(self):
        return Staff.objects.filter(is_published=True).order_by('time_create')


@login_required
def show_post_staff(request, post_id):
    post = get_object_or_404(Staff, pk=post_id)
    avatar = post.avatar.url
    comments = post.get_comments()
    album_list = post.get_album_list()
    album_wall_pk = get_object_or_404(album_list, title='Стена').pk
    ph_photos = get_object_or_404(album_list, title='Стена').images.all()
    type = post.type.values_list('name', flat=True)

    # Обработка комментариев
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.author_name = request.user.username
            comment.created_date = timezone.now()
            comment.save()
            Notification.objects.create(user=post.owner,
                                        notification_type='Новый комментарий: Стилист',
                                        text=f'У стилиста новый комментарий')
            return redirect('post_staff', post_id=post.pk)
    else:
        comment_form = CommentForm()

    context = {
        'ph_photos': ph_photos,
        'post': post,
        'avatar': avatar,
        'user': request.user,
        'comment_form': comment_form,
        'comments': comments,
        'album_list': album_list,
        'type': type,
        'album_wall_pk': album_wall_pk,
    }

    return render(request, 'post_staff.html', context=context)


def photo_editor_staff(request, pk, album_pk):
    post = get_object_or_404(Staff, pk=pk)
    albums = post.get_album_list()
    album = AlbumStaff.objects.get(pk=album_pk)
    photos = album.images.all()
    album_name = album.title

    # Создание альбомов
    if request.method == 'POST':
        create_album_form = AlbumForm(request.POST)
        if create_album_form.is_valid():
            album = create_album_form.save(commit=False)
            album.owner = post
            album.save()
            return redirect('photo_editor_staff', pk=post.pk, album_pk=album.pk)
    else:
        create_album_form = AlbumForm()

    # Обработка загрузки фотографий
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            images = request.FILES.getlist('images')
            for image in images:
                ImageStaff.objects.create(model=post,
                                       image=image, album=album)
            return redirect('photo_editor_staff', pk=post.pk, album_pk=album.pk)
    else:
        upload_form = UploadImageForm()

    context = {
        'albums': albums,
        'album_pk': album.pk,
        'photos': photos,
        'post': post,
        'album_name': album_name,
        'create_album_form': create_album_form,
        'upload_form': upload_form,

    }
    return render(request, 'photo_editor_staff.html', context)


@login_required
def create_staff(request):
    owner_id = request.user.id
    if Staff.objects.filter(owner_id=owner_id).exists():
        error_message = 'Фотограф уже зарегистрирован для данного пользователя'
        return render(request, 'create_staff.html', {'error_message': error_message})
    if request.method == 'POST':
        form = StaffForm(request.POST, request.FILES)
        if form.is_valid():
            staff = form.save(commit=False)
            staff.owner = request.user
            staff.save()
            form.save_m2m()
            album = AlbumStaff.objects.create(title='Стена', owner=staff)
            return redirect('post_staff', post_id=staff.pk)
    else:
        form = StaffForm()
    return render(request, 'create_staff.html', {'form': form, 'context': 'стилиста'})

@login_required
def edit_post_staff(request, post_id):
    model = Staff.objects.get(pk=post_id)
    if request.method == 'POST':
        form = StaffForm(request.POST, request.FILES, instance=model)
        if form.is_valid():
            form.save()
            return redirect('post_staff', post_id=post_id)
    else:
        form = StaffForm(instance=model)
    return render(request, 'edit_staff.html', {'form': form})


@login_required
def delete_photo(request, photo_id):
    photo = get_object_or_404(ImageStaff, pk=photo_id)
    if photo.model.owner != request.user:
        return JsonResponse({'status': 'error', 'message': 'Вы не можете удалить эту фотографию'})
    photo.delete()
    return JsonResponse({'status': 'ok', 'message': 'Фотография успешно удалена'})


@login_required
def album_delete_staff(request, pk, album_pk):
    post = get_object_or_404(Staff, pk=pk)
    album_list = post.get_album_list()
    album_wall_pk = get_object_or_404(album_list, title='Стена').pk
    album = get_object_or_404(AlbumStaff, pk=album_pk)
    if request.user == post.owner:
        album.delete()
    return redirect('photo_editor_staff', pk=post.pk, album_pk=album_wall_pk)


@login_required
def comment_delete_staff(request, pk):
    comment = get_object_or_404(CommentStaff, pk=pk)
    if request.user == comment.author:
        comment.delete()
    return redirect('post_staff', post_id=comment.post.pk)


def like_view(request, pk):
    post = get_object_or_404(Staff, pk=pk)
    if request.user.is_authenticated:
        if request.user in post.like.all():
            post.like.remove(request.user)
        else:
            post.like.add(request.user)
    return HttpResponseRedirect(reverse('post_staff', args=[str(pk)]))


@login_required
def liked_staff(request):
    liked_ph = request.user.likes.all()
    context = {
        'liked_ph': liked_ph
    }
    return render(request, 'liked_staff.html', context)


def load_photos(request, album_id):
    album = get_object_or_404(AlbumStaff, pk=album_id)
    photos = ImageStaff.objects.filter(album=album)
    photo_data = [{'id': p.pk, 'image': p.image.url} for p in photos]
    return JsonResponse({'photos': photo_data})


@require_POST
@csrf_exempt
def delete_photos(request):
    if request.method == 'POST':
        photo_ids = json.loads(request.body)
        for photo_id in photo_ids:
            photo = get_object_or_404(ImageStaff, pk=photo_id)
            photo.delete()
        return HttpResponse(status=200)
    return HttpResponseBadRequest()


@require_POST
def move_photos(request):
    album_id = request.POST.get('album_id')
    photo_ids = json.loads(request.POST.get('photos'))

    if album_id and photo_ids:
        album = AlbumStaff.objects.get(id=album_id)
        photos = ImageStaff.objects.filter(id__in=photo_ids)
        for photo in photos:
            photo.album = album
            photo.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})
