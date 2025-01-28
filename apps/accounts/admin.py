from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class UserAccountAdmin(UserAdmin):
    model = User
    list_display = ('email', 'first_name', 'is_verified', 'is_staff',  'is_active')
    list_filter = ('is_staff',  'is_verified',  'is_active')
    search_fields = ('email', 'first_name', 'last_name', 'phone_number', 'gender', 'photo')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone_number', 'gender', 'photo')}),

        # ('Social Links', {'fields': ('fiver', 'linkedin', 'facebook', 'github', 'portfolio')}),
        ('Permissions', {'fields': ('is_verified', 'is_ec_member', 'is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_general_member', 'is_staff',  'is_verified',  'is_active', 'is_ec_member')}
        ),
    )


admin.site.register(User, UserAccountAdmin)
admin.site.register(TemporaryOTP)
