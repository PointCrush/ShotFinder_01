from django_filters import *
from django import forms

from .models import *


class StudioFilter(FilterSet):

    city = CharFilter(field_name='city', lookup_expr='icontains', label='Город',
                      widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Studio
        fields = ['city']