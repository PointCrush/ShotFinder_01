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
from Photographers.filters import *
from Photographers.forms import *
from Photographers.models import *


# Create your views here.
class PhotographerPage(FilterView):
    model = Photographer
    template_name = 'ph_content.html'
    filterset_class = PhotographerFilter
    extra_context = {
        'title': 'Фотографы',
        'object': 'фотографа',
        'create': 'create_ph',
        'post': 'ph_post',
    }

    def get_queryset(self):
        return Photographer.objects.filter(is_published=True).order_by('time_create')


@login_required
def show_ph_post(request, post_id):
    post = get_object_or_404(Photographer, pk=post_id)
    avatar = post.avatar.url
    comments = post.get_comments()
    album_list = post.get_album_list()
    album_wall_pk = get_object_or_404(album_list, title='Стена').pk
    ph_photos = get_object_or_404(album_list, title='Стена').image_ph.all()
    genres = post.genre.values_list('name', flat=True)

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
                                        notification_type='Новый комментарий: Фотограф',
                                        text=f'У фотографа новый комментарий')
            return redirect('ph_post', post_id=post.pk)
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
        'genres': genres,
        'album_wall_pk': album_wall_pk,
    }

    return render(request, 'ph_post.html', context=context)


def ph_photo_editor(request, pk, album_pk):
    post = get_object_or_404(Photographer, pk=pk)
    albums = post.get_album_list()
    album = AlbumPh.objects.get(pk=album_pk)
    photos = album.image_ph.all()
    album_name = album.title

    # Создание альбомов
    if request.method == 'POST':
        create_album_form = AlbumForm(request.POST)
        if create_album_form.is_valid():
            album = create_album_form.save(commit=False)
            album.owner = post
            album.save()
            return redirect('ph_photo_editor', pk=post.pk, album_pk=album.pk)
    else:
        create_album_form = AlbumForm()

    # Обработка загрузки фотографий
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            images = request.FILES.getlist('images')
            for image in images:
                ImagePh.objects.create(model=post,
                                       image=image, album=album)
            return redirect('ph_photo_editor', pk=post.pk, album_pk=album.pk)
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
    return render(request, 'ph_photo_editor.html', context)


@login_required
def create_ph(request):
    owner_id = request.user.id
    if Photographer.objects.filter(owner_id=owner_id).exists():
        error_message = 'Фотограф уже зарегистрирован для данного пользователя'
        return render(request, 'create_ph.html', {'error_message': error_message})
    if request.method == 'POST':
        form = PhForm(request.POST, request.FILES)
        if form.is_valid():
            photographer = form.save(commit=False)
            photographer.owner = request.user
            photographer.save()
            form.save_m2m()
            album = AlbumPh.objects.create(title='Стена', owner=photographer)
            return redirect('ph_post', post_id=photographer.pk)
    else:
        form = PhForm()
    return render(request, 'create_ph.html', {'form': form, 'context': 'фотографа'})

@login_required
def edit_ph_post(request, post_id):
    model = Photographer.objects.get(pk=post_id)
    if request.method == 'POST':
        form = PhForm(request.POST, request.FILES, instance=model)
        if form.is_valid():
            form.save()
            return redirect('ph_post', post_id=post_id)
    else:
        form = PhForm(instance=model)
    return render(request, 'edit_ph.html', {'form': form})


@login_required
def delete_photo(request, photo_id):
    photo = get_object_or_404(ImagePh, pk=photo_id)
    if photo.model.owner != request.user:
        return JsonResponse({'status': 'error', 'message': 'Вы не можете удалить эту фотографию'})
    photo.delete()
    return JsonResponse({'status': 'ok', 'message': 'Фотография успешно удалена'})


@login_required
def ph_album_delete(request, pk, album_pk):
    post = get_object_or_404(Photographer, pk=pk)
    album_list = post.get_album_list()
    album_wall_pk = get_object_or_404(album_list, title='Стена').pk
    album = get_object_or_404(AlbumPh, pk=album_pk)
    if request.user == post.owner:
        album.delete()
    return redirect('ph_photo_editor', pk=post.pk, album_pk=album_wall_pk)


@login_required
def ph_comment_delete(request, pk):
    comment = get_object_or_404(CommentPh, pk=pk)
    if request.user == comment.author:
        comment.delete()
    return redirect('ph_post', post_id=comment.post.pk)


def like_view(request, pk):
    post = get_object_or_404(Photographer, pk=pk)
    if request.user.is_authenticated:
        if request.user in post.like.all():
            post.like.remove(request.user)
        else:
            post.like.add(request.user)
    return HttpResponseRedirect(reverse('ph_post', args=[str(pk)]))


@login_required
def liked_ph(request):
    liked_ph = request.user.likes.all()
    context = {
        'liked_ph': liked_ph
    }
    return render(request, 'ph_liked.html', context)


def load_photos(request, album_id):
    album = get_object_or_404(AlbumPh, pk=album_id)
    photos = ImagePh.objects.filter(album=album)
    photo_data = [{'id': p.pk, 'image': p.image.url} for p in photos]
    return JsonResponse({'photos': photo_data})


@require_POST
@csrf_exempt
def delete_photos(request):
    if request.method == 'POST':
        photo_ids = json.loads(request.body)
        for photo_id in photo_ids:
            photo = get_object_or_404(ImagePh, pk=photo_id)
            photo.delete()
        return HttpResponse(status=200)
    return HttpResponseBadRequest()


@require_POST
def move_photos(request):
    album_id = request.POST.get('album_id')
    photo_ids = json.loads(request.POST.get('photos'))

    if album_id and photo_ids:
        album = AlbumPh.objects.get(id=album_id)
        photos = ImagePh.objects.filter(id__in=photo_ids)
        for photo in photos:
            photo.album = album
            photo.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})
