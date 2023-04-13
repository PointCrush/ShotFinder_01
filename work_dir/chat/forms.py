from django import forms
from .models import *

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']

    content = forms.CharField(
        label='Сообщение',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )