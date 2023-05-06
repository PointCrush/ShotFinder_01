from django import forms
from .models import *


class LocationCreationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['city', 'title', 'description', 'way', ]

    city = forms.CharField(
        label='Город',
        max_length=250,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    title = forms.CharField(
        label='Название',
        max_length=250,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    description = forms.CharField(
        label='Описание',
        max_length=250,
        required=True,
        widget=forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
    )

    way = forms.CharField(
        label='Как добраться',
        max_length=250,
        required=False,
        widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
    )


class UploadImageForm(forms.ModelForm):
    images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True, 'class': 'form-control'}))

    class Meta:
        model = LocationImage
        fields = ['images']
