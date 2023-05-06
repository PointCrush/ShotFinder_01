from django import forms

from .models import *


class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['city', 'age', 'gender', 'type', 'tfp_photos', 'avatar', 'is_published', 'inst', 'vk', 'tg']

    city = forms.CharField(max_length=250, label='Город', widget=forms.TextInput(attrs={'class': 'form-control'}))
    age = forms.IntegerField(label='Возраст', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    gender = forms.ChoiceField(choices=Staff.GENDER_CHOICES, label='Пол',
                               widget=forms.Select(attrs={'class': 'form-select'}))
    type = forms.ModelMultipleChoiceField(queryset=StuffType.objects.all(), label='Тип',
                                          widget=forms.SelectMultiple(attrs={'class': 'form-select', 'size': '5'}))
    tfp_photos = forms.BooleanField(label='Сотрудничество по TFP',
                                    widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), required=False)
    avatar = forms.ImageField(label='Фото профиля', required=True,
                              widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    is_published = forms.BooleanField(label='Опубликовать',
                                      widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), required=False,
                                      initial=True)

    inst = forms.CharField(required=False, max_length=250, widget=forms.TextInput(attrs={'class': 'form-control'}))
    vk = forms.CharField(required=False, max_length=250, widget=forms.TextInput(attrs={'class': 'form-control'}))
    tg = forms.CharField(required=False, max_length=250, widget=forms.TextInput(attrs={'class': 'form-control'}))


class UploadImageForm(forms.ModelForm):
    images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True, 'class': 'form-control'}))

    class Meta:
        model = ImageStaff
        fields = ['images']


class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentStaff
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }


class AlbumForm(forms.ModelForm):
    class Meta:
        model = AlbumStaff
        fields = ['title']
        labels = {
            'title': 'Добавить альбом',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }


class MovePhotosForm(forms.Form):
    album = forms.ModelChoiceField(queryset=AlbumStaff.objects.all())
