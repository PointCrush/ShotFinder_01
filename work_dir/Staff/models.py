import os

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from multiupload.fields import MultiFileField


# Create your models here.
class Staff(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    city = models.CharField(max_length=250, null=True, verbose_name='Город')
    age = models.PositiveSmallIntegerField(verbose_name='Возраст', null=True)
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
        ('O', 'Другое'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M', verbose_name='Пол')

    type = models.ManyToManyField('StuffType')

    tfp_photos = models.BooleanField(default=False, verbose_name='Сотрудничество по ТФП', null=True)

    avatar = models.ImageField(upload_to='avatar/stuff/%Y/%m/%d/', blank=True, verbose_name='Фото профиля')
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True, verbose_name='Опубликовать')

    inst = models.CharField(max_length=50, null=True)
    vk = models.CharField(max_length=250, null=True)
    tg = models.CharField(max_length=50, null=True)

    like = models.ManyToManyField(User, blank=True, related_name='likes_staff')

    def get_album_list(self):
        albums = self.albums.all()
        return albums

    def get_comments(self):
        comments = self.comments.all()
        return comments

    def like_count(self):
        return self.like.count()

    # def __str__(self):
    #     return self.owner.username

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_id': self.pk})


class StuffType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class CommentStaff(models.Model):
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    author_name = models.CharField(max_length=50, null=True)
    post = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(null=True)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text


# {{{{{{{    БЛОК ОБРАБОТКИ ФОТОГРАФИЙ       }}}}}}}}}}}}}}}

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f'user_{instance.model.owner.username}/{timezone.now().strftime("%Y/%m/%d")}/{filename}'


class AlbumStaff(models.Model):
    owner = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='albums')
    title = models.CharField(max_length=255, default="Альбом")
    time_create = models.DateTimeField(auto_now_add=True)


class ImageStaff(models.Model):
    model = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True, related_name='photos')
    album = models.ForeignKey(AlbumStaff, on_delete=models.CASCADE, null=True, related_name='images')
    image = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
