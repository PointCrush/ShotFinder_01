from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import User
from Models.models import Model
from Photographers.models import Photographer
from Staff.models import Staff


# Create your models here.
# from django.contrib.auth.models import BaseUserManager
#
# class CustomUserManager(BaseUserManager):
#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError('The Email field must be set')
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_superuser(self, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         return self.create_user(email, password, **extra_fields)
#
#
# from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
# from django.db import models
#
# class CustomUser(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField(unique=True)
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     date_joined = models.DateTimeField(auto_now_add=True)
#     avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
#
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['first_name', 'last_name']
#
#     objects = CustomUserManager()
#
#     def __str__(self):
#         return self.email


def get_related_models(user):
    # Получите объекты Model, Photographer и Staff, связанные с пользователем
    user_model = Model.objects.filter(owner=user).first()
    user_photographer = Photographer.objects.filter(owner=user).first()
    user_staff = Staff.objects.filter(owner=user).first()

    # Объедините связанные модели в один список, исключая None
    models_related_to_user = [model for model in [user_model, user_photographer, user_staff] if model is not None]

    return models_related_to_user


def get_content_type_pk_tuples(models):
    content_type_pk_tuples = [(ContentType.objects.get_for_model(model), model.pk) for model in models]

    return content_type_pk_tuples


class HaveShots(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
