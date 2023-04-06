from django import forms
from .models import *
from django.core.exceptions import ValidationError
from PIL import Image
from io import BytesIO


class ProjectCreateForm(forms.ModelForm):
    class Meta:
        model = Project_01
        fields = ['name', 'my_profession', 'city', 'description', 'tfp', 'adult_only', 'price', 'looking_for',
                  'is_published']

    name = forms.CharField(
        label='Название проекта',
        max_length=250,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    my_profession = forms.ModelChoiceField(
        label='Я',
        queryset=Professions.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-select', 'size': '3'})
    )

    city = forms.CharField(
        label='Город',
        max_length=250,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    description = forms.CharField(
        label='О проекте',
        widget=forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
        required=False
    )

    adult_only = forms.BooleanField(
        label='(18+)',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    tfp = forms.BooleanField(
        label='Сотрудничество по ТФП',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    price = forms.CharField(
        label='Прайс',
        max_length=250,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    looking_for = forms.ModelMultipleChoiceField(
        label='Кого искать',
        queryset=Professions.objects.all(),
        required=True,
        widget=forms.SelectMultiple(attrs={'class': 'form-select', 'size': '5'})
    )

    is_published = forms.BooleanField(
        label='Опубликовать',
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )


class UploadImageForm(forms.ModelForm):
    images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True, 'class': 'form-control'}))

    class Meta:
        model = ImageProject01
        fields = ['images']

