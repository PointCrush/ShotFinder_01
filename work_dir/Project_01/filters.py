from django_filters import *
from django import forms

from .models import *


class ProjectFilter(FilterSet):
    BOOLEAN_CHOICES = [
        (None, 'Не важно'),
        (True, 'Да'),
        (False, 'Нет')
    ]
    city = CharFilter(field_name='city', lookup_expr='icontains', label='Город',
                      widget=forms.TextInput(attrs={'class': 'form-control'}))

    name = CharFilter(field_name='name', lookup_expr='icontains', label='Название проекта',
                      widget=forms.TextInput(attrs={'class': 'form-control'}))

    looking_for = ModelMultipleChoiceFilter(field_name='genre', to_field_name='id', queryset=Professions.objects.all(),
                                      label='Кто требуется',
                                      widget=forms.SelectMultiple(attrs={'class': 'form-select', 'size': '5'}))
    tfp = BooleanFilter(field_name='tfp',
                                    widget=forms.Select(choices=BOOLEAN_CHOICES, attrs={'class': 'form-select'}),
                                    label='ТФП проекты')
    adult_only = BooleanFilter(field_name='adult_only',
                                    widget=forms.Select(choices=BOOLEAN_CHOICES, attrs={'class': 'form-select'}),
                                    label='Проекты 18+')
    class Meta:
        model = Project_01
        fields = ['city', 'name', 'looking_for', 'tfp', 'adult_only']