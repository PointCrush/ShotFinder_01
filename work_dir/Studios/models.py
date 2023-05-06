from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Studio(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    telephone_number = models.CharField(max_length=100, null=True)
    mail = models.CharField(max_length=100, null=True)
    logo = models.ImageField(upload_to='studio_logo_directory_path', null=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    schedule = models.TextField(null=True)
    way = models.TextField(null=True)
    price = models.TextField(null=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        r = self.city + ' ' + self.title
        return r


def studio_logo_directory_path(instance, filename):
    return f'studios/logo/{instance.studio.title}/{instance.studio.owner_username}/{timezone.now().strftime("%Y/%m/%d")}/{filename}'


def studio_directory_path(instance, filename):
    return f'studios/{instance.studio.owner.username}/{instance.studio.title}/{timezone.now().strftime("%Y/%m/%d")}/{filename}'


class StudioImage(models.Model):
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE, null=True, related_name='photos')
    image = models.ImageField(upload_to=studio_directory_path)
    created_at = models.DateTimeField(auto_now_add=True)


class HaveStudio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
