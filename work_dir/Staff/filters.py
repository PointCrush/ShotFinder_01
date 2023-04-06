from django_filters import *
from django import forms


from .models import *

class StaffFilter(FilterSet):
    type = ModelMultipleChoiceFilter(field_name='type', to_field_name='id', queryset=StuffType.objects.all(),
                                      label='Специальность',
                                      widget=forms.SelectMultiple(attrs={'class': 'form-select', 'size': '5'}))
    city = CharFilter(field_name='city', lookup_expr='icontains', label='Город', widget=forms.TextInput(attrs={'class': 'form-control'}))
    gender = ChoiceFilter(choices=Staff.GENDER_CHOICES, label='Пол', widget=forms.Select(attrs={'class': 'form-select'}))
    tfp_photos = BooleanFilter(label='Сотрудничество по TFP', widget=forms.NullBooleanSelect(attrs={'class': 'form-select'}))

    class Meta:
        model = Staff
        fields = ['city', 'gender', 'tfp_photos']