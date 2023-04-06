from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


# Create your models here.
class Project_01(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    my_profession = models.ForeignKey('Professions', on_delete=models.CASCADE, related_name='owner_role', null=True)
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    description = models.TextField(null=True)
    tfp = models.BooleanField(default=False)
    adult_only = models.BooleanField(default=False)
    price = models.CharField(max_length=255, null=True)
    looking_for = models.ManyToManyField('Professions', related_name='looking_for')
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} in {self.city}"

    def get_my_projects(self, user):
        return Project_01.objects.filter(owner=user)


class Professions(models.Model):
    name = models.CharField(max_length=50)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    link = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f"{self.name}"


class ProjectMember(models.Model):
    project = models.ForeignKey(Project_01, on_delete=models.CASCADE, related_name='members')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    member = GenericForeignKey('content_type', 'object_id')
    role = models.CharField(max_length=50)
    link = models.CharField(max_length=50, null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_approved = models.BooleanField(default=False)

    class Meta:
        unique_together = ('project', 'content_type', 'object_id')

    def __str__(self):
        return f"{self.member.owner} in {self.project} as {self.role} - {self.is_approved}"


def project_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f'projects/city_{instance.model.city}/project_{instance.model.name}'


class ImageProject01(models.Model):
    model = models.ForeignKey(Project_01, on_delete=models.CASCADE, null=True, related_name='references')
    image = models.ImageField(upload_to=project_directory_path, null=True, blank=True)
