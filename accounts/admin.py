from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


# class CustomUserAdmin(UserAdmin):
#     list_display = ('email', 'first_name', 'last_name', 'middle_name', 'avatar', 'role', 'phone', 'is_staff',
#                     'is_active', 'date_joined', 'last_login', 'address')
#     list_filter = ('is_staff', 'is_active', 'date_joined', 'last_login', 'role')
#     search_fields = ('email', 'first_name', 'last_name', 'middle_name', 'phone', 'address')
#     ordering = ('email', 'first_name', 'last_name', 'middle_name', 'phone', 'address')
#
#
# admin.site.register(User, CustomUserAdmin)

class UserAdminCustom(UserAdmin):
    model = User
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'middle_name', 'avatar', 'role')}),
        ('Contact info', {'fields': ('phone', 'address', 'city')}),
        ('Additional info', {'fields': ('date_of_birth', 'bio', 'website')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('id', 'email', 'first_name', 'last_name', 'middle_name', 'avatar', 'role', 'phone', 'is_staff',
                    'is_active', 'date_joined', 'last_login', 'address')
    list_filter = ('is_staff', 'is_active', 'date_joined', 'last_login', 'role')
    search_fields = ('email', 'first_name', 'last_name', 'middle_name', 'phone', 'address')
    ordering = ('email', 'first_name', 'last_name', 'middle_name', 'phone', 'address')
    click = ('email', 'first_name', 'last_name', 'middle_name', 'phone', 'address')


admin.site.register(User, UserAdminCustom)
