from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import *

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Почта')
    first_name = forms.CharField(label='Имя', max_length=30, required=True)
    last_name = forms.CharField(label='Фамилия', max_length=30, required=True)

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].error_messages = {'required': 'Please enter your email address.'}
        self.fields['first_name'].error_messages = {'required': 'Please enter your first name.'}
        self.fields['last_name'].error_messages = {'required': 'Please enter your last name.'}

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')

    first_name = forms.CharField(
        label='Имя',
        max_length=250,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    last_name = forms.CharField(
        label='Фамилия',
        max_length=250,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин', max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label='Пароль', max_length=30,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))
