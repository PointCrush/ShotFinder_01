from django import forms
from .models import Invite


class InviteForm(forms.ModelForm):
    class Meta:
        model = Invite
        fields = ('content', 'project')

    content = forms.CharField(
        label='Текст приглашения',
        max_length=250,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    project = forms.ModelChoiceField(
        label='Выберите проект',
        queryset=None,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['project'].queryset = user.projects.all()
        self.fields['project'].empty_label = None
