from django_filters import *
from django import forms


from .forms import AgeRangeWidget
from .models import *


class ModelFilter(FilterSet):
    city = CharFilter(field_name='city', lookup_expr='icontains', label='Город',
                      widget=forms.TextInput(attrs={'class': 'form-control'}))
    clothing_size = ChoiceFilter(choices=Model.CLOTHING_SIZE, label='Размер одежды', widget=forms.Select(attrs={'class': 'form-select'}))
    gender = ChoiceFilter(choices=Model.GENDER_CHOICES, label='Пол', widget=forms.Select(attrs={'class': 'form-select'}))
    age = RangeFilter(field_name='age', lookup_expr=['gte', 'lte'], widget=AgeRangeWidget(), label='Возраст')
    height = RangeFilter(field_name='height', lookup_expr=['gte', 'lte'], widget=AgeRangeWidget(), label='Рост')
    # weight = RangeFilter(field_name='weight', lookup_expr=['gte', 'lte'], widget=AgeRangeWidget(), label='Вес')
    # bust = RangeFilter(field_name='bust', lookup_expr=['gte', 'lte'], widget=AgeRangeWidget(), label='Обхват груди')
    # waist = RangeFilter(field_name='waist', lookup_expr=['gte', 'lte'], widget=AgeRangeWidget(), label='Обхват талии')
    # hips = RangeFilter(field_name='hips', lookup_expr=['gte', 'lte'], widget=AgeRangeWidget(), label='Обхват бедер')
    shoe_size = RangeFilter(field_name='shoe_size', lookup_expr=['gte', 'lte'], widget=AgeRangeWidget(),
                            label='Размер ноги')
    BOOLEAN_CHOICES = [
        (None, 'Не важно'),
        (True, 'Да'),
        (False, 'Нет')
    ]
    tattoo = BooleanFilter(field_name='tattoo',
                                        widget=forms.Select(choices=BOOLEAN_CHOICES, attrs={'class': 'form-select'}),
                                        label='Наличие тату')
    in_under_photos = BooleanFilter(field_name='in_under_photos',
                                    widget=forms.Select(choices=BOOLEAN_CHOICES, attrs={'class': 'form-select'}),
                                    label='Согласие на фото в нижнем белье/купальнике')
    nu_photos = BooleanFilter(field_name='nu_photos',
                              widget=forms.Select(choices=BOOLEAN_CHOICES, attrs={'class': 'form-select'}),
                              label='Согласие на ню-фото (18+)')
    tfp_photos = BooleanFilter(field_name='tfp_photos',
                               widget=forms.Select(choices=BOOLEAN_CHOICES, attrs={'class': 'form-select'}),
                               label='Сотрудничество по ТФП')

    class Meta:
        model = Model
        fields = ['age', 'height', 'shoe_size', 'city', 'gender', 'clothing_size', 'tattoo', 'in_under_photos', 'nu_photos', 'tfp_photos']

