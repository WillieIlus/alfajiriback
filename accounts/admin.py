from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User

# class CustomUserAdmin(UserAdmin):
#     list_display = ('email', 'first_name', 'last_name', 'middle_name', 'avatar', 'role', 'phone', 'is_staff', 'is_active', 'date_joined', 'last_login', 'address')
#     list_filter = ('email', 'first_name', 'last_name', 'middle_name', 'avatar', 'role', 'phone', 'is_staff', 'is_active', 'date_joined', 'last_login', 'address')
#     search_fields = ('email', 'first_name', 'last_name', 'middle_name', 'avatar', 'role', 'phone', 'is_staff', 'is_active', 'date_joined', 'last_login', 'address')
#     ordering = ('email', 'first_name', 'last_name', 'middle_name', 'avatar', 'role', 'phone', 'is_staff', 'is_active', 'date_joined', 'last_login', 'address')


# admin.site.register(User, CustomUserAdmin)
admin.site.register(User)

