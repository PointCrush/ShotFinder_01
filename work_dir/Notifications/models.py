from django.db import models
from django.contrib.auth.models import User

from Project_01.models import Project_01, Professions


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=255)
    text = models.TextField()
    status = models.CharField(max_length=20, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Invite(models.Model):
    whom = models.ForeignKey(User, on_delete=models.CASCADE, related_name='got_invites')
    from_whom = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invites')
    title = models.CharField(max_length=255)
    content = models.TextField()
    project = models.ForeignKey(Project_01, on_delete=models.CASCADE)
    role = models.ForeignKey(Professions, on_delete=models.DO_NOTHING, null=True)
    status = models.CharField(max_length=20, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('project', 'whom')