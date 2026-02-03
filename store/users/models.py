from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
# users/models.py



class User(AbstractUser):
    middle_name = models.CharField(max_length=150, blank=True, verbose_name="Отчество")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    address = models.TextField(blank=True, verbose_name="Адрес доставки")

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
