from django_filters import *
from django import forms

from .models import *


class PhotographerFilter(FilterSet):
    BOOLEAN_CHOICES = [
        (None, 'Не важно'),
        (True, 'Да'),
        (False, 'Нет')
    ]
    city = CharFilter(field_name='city', lookup_expr='icontains', label='Город',
                      widget=forms.TextInput(attrs={'class': 'form-control'}))
    gender = ChoiceFilter(choices=Photographer.GENDER_CHOICES, label='Пол',
                          widget=forms.Select(attrs={'class': 'form-select'}))
    genre = ModelMultipleChoiceFilter(field_name='genre', to_field_name='id', queryset=ShootingGenre.objects.all(),
                                      label='Жанр',
                                      widget=forms.SelectMultiple(attrs={'class': 'form-select', 'size': '5'}))
    tfp_photos = BooleanFilter(field_name='tfp_photos',
                                    widget=forms.Select(choices=BOOLEAN_CHOICES, attrs={'class': 'form-select'}),
                                    label='Согласие на сотрудничество по модели ТФП')
    in_under_photos = BooleanFilter(field_name='in_under_photos',
                                    widget=forms.Select(choices=BOOLEAN_CHOICES, attrs={'class': 'form-select'}),
                                    label='Согласие на фото в нижнем белье/купальнике')
    nu_photos = BooleanFilter(field_name='nu_photos',
                                    widget=forms.Select(choices=BOOLEAN_CHOICES, attrs={'class': 'form-select'}),
                                    label='Ню-фотограф (18+)')

    class Meta:
        model = Photographer
        fields = ['city', 'gender', 'genre', 'tfp_photos', 'in_under_photos', 'nu_photos']
