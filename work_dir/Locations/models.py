from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


class Location(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    city = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    description = models.TextField()
    way = models.TextField()
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


def location_directory_path(instance, filename):
    return f'location/{instance.location.owner.username}/{instance.location.title}/{timezone.now().strftime("%Y/%m/%d")}/{filename}'


class LocationImage(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, related_name='photos')
    image = models.ImageField(upload_to=location_directory_path)
    created_at = models.DateTimeField(auto_now_add=True)