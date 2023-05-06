from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm

from .models import *


# class CustomUserCreationForm(UserCreationForm):
#     email = forms.EmailField(required=True, label='Почта')
#     first_name = forms.CharField(label='Имя', max_length=30, required=True)
#     last_name = forms.CharField(label='Фамилия', max_length=30, required=True)
#
#     class Meta:
#         model = User
#         fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name',)
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['username'].widget.attrs.update({'class': 'form-control'})
#         self.fields['password1'].widget.attrs.update({'class': 'form-control'})
#         self.fields['password2'].widget.attrs.update({'class': 'form-control'})
#         self.fields['email'].widget.attrs.update({'class': 'form-control'})
#         self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
#         self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
#         self.fields['email'].error_messages = {'required': 'Please enter your email address.'}
#         self.fields['first_name'].error_messages = {'required': 'Please enter your first name.'}
#         self.fields['last_name'].error_messages = {'required': 'Please enter your last name.'}
#
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.email = self.cleaned_data['email']
#         user.first_name = self.cleaned_data['first_name']
#         user.last_name = self.cleaned_data['last_name']
#         if commit:
#             user.save()
#         return user


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(label='Имя', max_length=20, required=True)
    last_name = forms.CharField(label='Фамилия', max_length=20, required=True)

    def signup(self, request, user):
        # Сохраняем дополнительные данные в профиле пользователя
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Этот email уже зарегистрирован в системе.")
        return email


class CustomSocialSignupForm(SocialSignupForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Этот email уже зарегистрирован в системе.")
        return email


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')

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

    username = forms.CharField(
        label='Имя пользователя',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
