from django.contrib.auth.forms import UserCreationForm

from .models import User, ReturningRequest, Item
from django.forms import ModelForm, TextInput, PasswordInput, EmailInput
from django import forms


class RegistrationForm(UserCreationForm):
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(attrs={
        'class': '',
        'placeholder': 'Повтор пароля',
        'required': 'required'
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1']
        widgets = {
            "username": TextInput(attrs={
                'class': '',
                'placeholder': 'Логин',
                'required': 'required'
            }),
            "email": EmailInput(attrs={
                'class': '',
                'placeholder': 'Email',
                'required': 'required'
            }),
            "password1": PasswordInput(attrs={
                'placeholder': 'Пароль',
                'class': '',
                'required': 'required'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        password11 = cleaned_data.get('password1')
        password22 = cleaned_data.get('password2')
        if password11 and password22 and password11 != password22:
            self.add_error('password2', 'Пароли не совпадают')
