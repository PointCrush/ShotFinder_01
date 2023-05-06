from django import forms
from .models import *


class StudioCreationForm(forms.ModelForm):
    class Meta:
        model = Studio
        fields = ['city', 'address', 'title', 'telephone_number', 'mail', 'logo', 'description', 'schedule', 'way',
                  'price', ]

    city = forms.CharField(
        label='Город',
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    title = forms.CharField(
        label='Название',
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    description = forms.CharField(
        label='Описание',
        required=True,
        widget=forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
    )

    way = forms.CharField(
        label='Как добраться',
        required=False,
        widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
    )

    schedule = forms.CharField(
        label='Время работы',
        required=False,
        widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
    )

    price = forms.CharField(
        label='Цены',
        required=False,
        widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
    )

    address = forms.CharField(
        label='Адрес',
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    telephone_number = forms.CharField(
        label='Номер телефона',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    mail = forms.CharField(
        label='Адрес электронной почты',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    logo = forms.ImageField(
        label='Логотип',
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )


class UploadImageForm(forms.ModelForm):
    images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True, 'class': 'form-control'}))

    class Meta:
        model = StudioImage
        fields = ['images']
