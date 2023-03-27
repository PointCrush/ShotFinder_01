from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


# Create your models here.
class Model(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    city = models.CharField(max_length=250, null=True, verbose_name='Город')
    age = models.PositiveSmallIntegerField(verbose_name='Возраст')
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
        ('O', 'Другое'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M', verbose_name='Пол')

    height = models.PositiveSmallIntegerField(verbose_name='Рост')
    weight = models.PositiveSmallIntegerField(verbose_name='Вес')
    bust = models.PositiveSmallIntegerField(blank=True, verbose_name='Обхват груди')
    waist = models.PositiveSmallIntegerField(blank=True, verbose_name='Обхват талии')
    hips = models.PositiveSmallIntegerField(blank=True, verbose_name='Обхват бедер')
    shoe_size = models.PositiveSmallIntegerField(blank=True, verbose_name='Размер ноги')
    CLOTHING_SIZE = [
        ('XXS', 'XXS'),
        ('XS', 'XS'),
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
        ('XXL', 'XXL'),
        ('XXXL', 'XXXL'),
    ]
    clothing_size = models.CharField(max_length=4, choices=CLOTHING_SIZE, default='M', verbose_name='Размер одежды')

    hair_color = models.CharField(max_length=30, verbose_name='Цвет волос')
    eye_color = models.CharField(max_length=30, verbose_name='Цвет глаз')
    tattoo = models.BooleanField(default=True, verbose_name='Наличие тату')
    tattoo_description = models.CharField(max_length=200, blank=True,
                                          verbose_name='Если имеются тату, то на каких местах')

    in_under_photos = models.BooleanField(default=False, verbose_name='Согласие на фото в нижнем белье/купальнике')
    nu_photos = models.BooleanField(default=False, verbose_name='Согласие на ню-фото (18+)')
    tfp_photos = models.BooleanField(default=False, verbose_name='Сотрудничество по ТФП', null=True)

    avatar = models.ImageField(upload_to='avatar/model/%Y/%m/%d/', blank=True, verbose_name='Фото профиля')
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True, verbose_name='Опубликовать')

    inst = models.CharField(max_length=50, null=True)
    vk = models.CharField(max_length=250, null=True)
    tg = models.CharField(max_length=50, null=True)

    like = models.ManyToManyField(User, blank=True, related_name='likes')

    def get_album_list(self):
        albums = self.albums.all()
        return albums

    def get_comments(self):
        comments = self.comments.all()
        return comments

    def like_count(self):
        return self.like.count()

    def __str__(self):
        return self.owner.username

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_id': self.pk})


class CommentModel(models.Model):
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    author_name = models.CharField(max_length=50, null=True)
    post = models.ForeignKey(Model, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(null=True)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f'user_{instance.model.owner.username}/{timezone.now().strftime("%Y/%m/%d")}/{filename}'


class AlbumModel(models.Model):
    owner = models.ForeignKey(Model, on_delete=models.CASCADE, related_name='albums', null=True)
    title = models.CharField(max_length=255, default="Альбом")
    time_create = models.DateTimeField(auto_now_add=True)


class ImageModel(models.Model):
    model = models.ForeignKey(Model, on_delete=models.CASCADE, null=True, related_name='photos')
    album = models.ForeignKey(AlbumModel, on_delete=models.CASCADE, null=True, related_name='album')
    image = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
