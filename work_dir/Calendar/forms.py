from django import forms
from .models import *


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'content', 'event', 'is_published']

    title = forms.CharField(
        label='Событие',
        max_length=250,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    content = forms.CharField(
        label='Содержание',
        max_length=250,
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'})
    )

    event = forms.BooleanField(
        label='Свободный/Занят',
        required=False,
        initial=False,
        widget=forms.RadioSelect(choices=[(False, 'Свободен'), (True, 'Занят')])
    )

    is_published = forms.BooleanField(
        label='Видно всем',
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_is_published_{{ day }}'})
    )

