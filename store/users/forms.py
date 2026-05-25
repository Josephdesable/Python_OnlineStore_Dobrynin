from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    # Явно объявляем поля ФИО для правильного порядка и подписей
    first_name = forms.CharField(max_length=150, label="Имя")
    last_name = forms.CharField(max_length=150, label="Фамилия")
    middle_name = forms.CharField(max_length=150, label="Отчество", required=False)
    
    address = forms.CharField(widget=forms.Textarea, label="Адрес доставки")
    phone = forms.CharField(max_length=20, label="Телефон")

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "middle_name",
            "phone",
            "address",
            "password1",
            "password2",
        )
