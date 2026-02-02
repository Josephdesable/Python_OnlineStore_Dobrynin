# users/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    name = forms.CharField(max_length=100, label="ФИО")
    address = forms.CharField(widget=forms.Textarea, label="Адрес")
    phone = forms.CharField(max_length=20, label="Телефон")

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "name",
            "address",
            "phone",
            "password1",
            "password2",
        )
