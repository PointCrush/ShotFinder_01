from django.db import models
from django.contrib.auth.models import User

from Project_01.models import Project_01


class Event(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    project_link = models.ForeignKey(Project_01, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200, null=True)
    content = models.TextField(null=True)
    date = models.DateField(null=True)
    event = models.BooleanField(default=False, null=True)
    is_published = models.BooleanField(default=True)


class Note(models.Model):
    title = models.CharField(max_length=200, null=True)
    content = models.TextField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)
