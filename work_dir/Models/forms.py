from django import forms
from .models import *


class CreateModelForm(forms.ModelForm):
    class Meta:
        model = Model
        fields = ['city', 'age', 'gender', 'height', 'weight', 'bust', 'waist', 'hips', 'shoe_size',
                  'clothing_size', 'hair_color', 'eye_color', 'tattoo', 'tattoo_description', 'in_under_photos',
                  'nu_photos', 'tfp_photos', 'avatar', 'is_published', 'inst', 'vk', 'tg']

        widgets = {
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'height': forms.NumberInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'bust': forms.NumberInput(attrs={'class': 'form-control'}),
            'waist': forms.NumberInput(attrs={'class': 'form-control'}),
            'hips': forms.NumberInput(attrs={'class': 'form-control'}),
            'shoe_size': forms.NumberInput(attrs={'class': 'form-control'}),
            'clothing_size': forms.Select(attrs={'class': 'form-control'}),
            'hair_color': forms.TextInput(attrs={'class': 'form-control'}),
            'eye_color': forms.TextInput(attrs={'class': 'form-control'}),
            'tattoo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tattoo_description': forms.TextInput(attrs={'class': 'form-control'}),
            'in_under_photos': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'nu_photos': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tfp_photos': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control', 'required': True}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'inst': forms.TextInput(attrs={'class': 'form-control', 'required': False}),
            'vk': forms.TextInput(attrs={'class': 'form-control', 'required': False}),
            'tg': forms.TextInput(attrs={'class': 'form-control', 'required': False}),
        }


class AgeRangeWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = (
            forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'От'}),
            forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'До'}),
        )
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.start, value.stop]
        else:
            return [None, None]

    def format_output(self, rendered_widgets):
        return '<div class="input-group">' + \
            '<div class="input-group-prepend">' + \
            '<span class="input-group-text">От</span>' + \
            '</div>' + \
            rendered_widgets[0] + \
            '<div class="input-group-append">' + \
            '<span class="input-group-text">До</span>' + \
            '</div>' + \
            rendered_widgets[1] + \
            '</div>'


class UploadImageForm(forms.ModelForm):
    images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True, 'class': 'form-control'}))

    class Meta:
        model = ImageModel
        fields = ['images']


class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentModel
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }


class AlbumForm(forms.ModelForm):
    class Meta:
        model = AlbumModel
        fields = ['title']
        labels = {
            'title': 'Добавить альбом',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }


class MovePhotosForm(forms.Form):
    album = forms.ModelChoiceField(queryset=AlbumModel.objects.all())


class EditModelForm(forms.ModelForm):
    class Meta:
        model = Model
        fields = ('city', 'age', 'gender', 'height', 'weight', 'bust', 'waist', 'hips', 'shoe_size',
                  'clothing_size', 'hair_color', 'eye_color', 'tattoo', 'tattoo_description', 'in_under_photos',
                  'nu_photos', 'tfp_photos', 'avatar', 'is_published', 'inst', 'vk', 'tg')

        widgets = {
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'height': forms.NumberInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'bust': forms.NumberInput(attrs={'class': 'form-control'}),
            'waist': forms.NumberInput(attrs={'class': 'form-control'}),
            'hips': forms.NumberInput(attrs={'class': 'form-control'}),
            'shoe_size': forms.NumberInput(attrs={'class': 'form-control'}),
            'clothing_size': forms.Select(attrs={'class': 'form-control'}),
            'hair_color': forms.TextInput(attrs={'class': 'form-control'}),
            'eye_color': forms.TextInput(attrs={'class': 'form-control'}),
            'tattoo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tattoo_description': forms.TextInput(attrs={'class': 'form-control'}),
            'in_under_photos': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'nu_photos': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tfp_photos': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'inst': forms.TextInput(attrs={'class': 'form-control'}),
            'vk': forms.TextInput(attrs={'class': 'form-control'}),
            'tg': forms.TextInput(attrs={'class': 'form-control'}),
        }
