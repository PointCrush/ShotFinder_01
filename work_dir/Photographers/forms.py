from django import forms
from .models import *


class PhForm(forms.ModelForm):
    class Meta:
        model = Photographer
        fields = ['city', 'age', 'gender', 'genre', 'about', 'in_under_photos', 'nu_photos', 'tfp_photos', 'avatar', 'is_published']

    city = forms.CharField(
        label='Город',
        max_length=250,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    age = forms.IntegerField(
        label='Возраст',
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    gender = forms.ChoiceField(
        label='Пол',
        choices=Photographer.GENDER_CHOICES,
        initial='M',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    genre = forms.ModelMultipleChoiceField(
        label='Жанр фотосъемки',
        queryset=ShootingGenre.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-select', 'size': '5'})
    )

    about = forms.CharField(
        label='О себе',
        widget=forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
        required=False
    )

    in_under_photos = forms.BooleanField(
        label='Согласие на фото в нижнем белье/купальнике',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    nu_photos = forms.BooleanField(
        label='Согласие на ню-фото (18+)',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    tfp_photos = forms.BooleanField(
        label='Сотрудничество по ТФП',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    avatar = forms.ImageField(
        label='Фото профиля',
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    is_published = forms.BooleanField(
        label='Опубликовать',
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

class UploadImageForm(forms.ModelForm):
    images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = ImagePh
        fields = ['images']


class CommentForm(forms.ModelForm):

    class Meta:
        model = CommentPh
        fields = ('text', )
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3}),
        }

class AlbumForm(forms.ModelForm):
    class Meta:
        model = AlbumPh
        fields = ['title',]
        labels = {
            'title': 'Добавить альбом',
        }

class MovePhotosForm(forms.Form):
    album = forms.ModelChoiceField(queryset=AlbumPh.objects.all())