from django.contrib import admin

# Register your models here.
# users/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'middle_name', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительно', {'fields': ('middle_name', 'address', 'phone')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Дополнительно', {'fields': ('middle_name', 'address', 'phone')}),
    )
