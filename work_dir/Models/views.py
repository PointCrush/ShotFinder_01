import json

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django_filters.views import FilterView

from Models.filters import *
from Models.forms import *
from Models.models import *


# Create your views here.
class ModelsPage(FilterView):
    model = Model
    template_name = 'content.html'
    filterset_class = ModelFilter
    extra_context = {
        'title': 'Модели',
        'object': 'модели',
        'create': 'create_model',
        'post': 'model_post',
    }

    def get_queryset(self):
        return Model.objects.filter(is_published=True).order_by('time_create')


@login_required
def show_model_post(request, post_id):
    post = get_object_or_404(Model, pk=post_id)
    avatar = post.avatar.url
    comments = post.get_comments()
    album_list = post.get_album_list()
    album_wall_pk = get_object_or_404(album_list, title='Стена').pk
    model_photos = get_object_or_404(album_list, title='Стена').album.all()


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
            return redirect('model_post', post_id=post.pk)
    else:
        comment_form = CommentForm()

    # Обработка загрузки фотографий
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            all_album, created = AlbumModel.objects.get_or_create(owner=post, title='Стена')
            images = request.FILES.getlist('images')  # get list of uploaded images
            for image in images:
                ImageModel.objects.create(model=request.user.model,
                                          image=image, album=all_album)  # create Image instance for each uploaded image
            return redirect('model_post', post_id=post.pk)
    else:
        upload_form = UploadImageForm()

    context = {
        'model_photos': model_photos,
        'post': post,
        'avatar': avatar,
        'user': request.user,
        'upload_form': upload_form,
        'comment_form': comment_form,
        'comments': comments,
        'album_list': album_list,
        'album_wall_pk': album_wall_pk,
    }

    return render(request, 'model_post.html', context=context)


def photo_editor(request, pk, album_pk):
    post = get_object_or_404(Model, pk=pk)
    albums = post.get_album_list()
    album = AlbumModel.objects.get(pk=album_pk)
    photos = album.album.all()
    album_name = album.title

    # Создание альбомов
    if request.method == 'POST':
        create_album_form = AlbumForm(request.POST)
        if create_album_form.is_valid():
            album = create_album_form.save(commit=False)
            album.owner = request.user.model
            album.save()
            return redirect('photo_editor', pk=post.pk, album_pk=album.pk)
    else:
        create_album_form = AlbumForm()

    # Обработка загрузки фотографий
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            images = request.FILES.getlist('images')
            for image in images:
                ImageModel.objects.create(model=post,
                                          image=image, album=album)
            return redirect('photo_editor', pk=post.pk, album_pk=album.pk)
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
    return render(request, 'photo_editor.html', context)


@login_required
def create_model(request):
    owner_id = request.user.id
    if Model.objects.filter(owner_id=owner_id).exists():
        error_message = 'Модель уже зарегистрирован/а для данного пользователя'
        return render(request, 'create_model.html', {'error_message': error_message})
    if request.method == 'POST':
        form = CreateModelForm(request.POST, request.FILES)
        if form.is_valid():
            model = form.save(commit=False)
            model.owner = request.user
            model.save()
            album = AlbumModel.objects.create(title='Стена', owner=model)
            return redirect('model_post', post_id=model.pk)
    else:
        form = CreateModelForm()
    return render(request, 'create_model.html', {'form': form, 'context': 'модели'})

@login_required
def edit_model_post(request, post_id):
    model = Model.objects.get(pk=post_id)
    if request.method == 'POST':
        form = EditModelForm(request.POST, request.FILES, instance=model)
        if form.is_valid():
            form.save()
            return redirect('model_post', post_id=post_id)
    else:
        form = EditModelForm(instance=model)
    return render(request, 'edit_model.html', {'form': form})



@login_required
def delete_photo(request, photo_id):
    photo = get_object_or_404(ImageModel, pk=photo_id)
    if photo.model.owner != request.user:
        return JsonResponse({'status': 'error', 'message': 'Вы не можете удалить эту фотографию'})
    photo.delete()
    return JsonResponse({'status': 'ok', 'message': 'Фотография успешно удалена'})


@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(CommentModel, pk=pk)
    if request.user == comment.author:
        comment.delete()
    return redirect('model_post', post_id=comment.post.pk)

@login_required
def album_delete(request, pk, album_pk):
    post = get_object_or_404(Model, pk=pk)
    album_list = post.get_album_list()
    album_wall_pk = get_object_or_404(album_list, title='Стена').pk
    album = get_object_or_404(AlbumModel, pk=album_pk)
    if request.user == post.owner:
        album.delete()
    return redirect('photo_editor', pk=post.pk, album_pk=album_wall_pk)


def like_view(request, pk):
    post = get_object_or_404(Model, pk=pk)
    if request.user.is_authenticated:
        if request.user in post.like.all():
            post.like.remove(request.user)
        else:
            post.like.add(request.user)
    return HttpResponseRedirect(reverse('model_post', args=[str(pk)]))


@login_required
def liked_models(request):
    liked_models = request.user.likes.all()
    context = {
        'liked_models': liked_models
    }
    return render(request, 'ph_liked.html', context)



def load_photos(request, album_id):
    album = get_object_or_404(AlbumModel, pk=album_id)
    photos = ImageModel.objects.filter(album=album)
    photo_data = [{'id': p.pk, 'image': p.image.url} for p in photos]
    return JsonResponse({'photos': photo_data})


@require_POST
@csrf_exempt
def delete_photos(request):
    if request.method == 'POST':
        photo_ids = json.loads(request.body)
        for photo_id in photo_ids:
            photo = get_object_or_404(ImageModel, pk=photo_id)
            photo.delete()
        return HttpResponse(status=200)
    return HttpResponseBadRequest()


@require_POST
def move_photos(request):
    album_id = request.POST.get('album_id')
    photo_ids = json.loads(request.POST.get('photos'))

    if album_id and photo_ids:
        album = AlbumModel.objects.get(id=album_id)
        photos = ImageModel.objects.filter(id__in=photo_ids)
        for photo in photos:
            photo.album = album
            photo.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})
