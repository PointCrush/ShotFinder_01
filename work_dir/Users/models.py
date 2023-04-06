from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import User
from Models.models import Model
from Photographers.models import Photographer
from Staff.models import Staff


# Create your models here.

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
