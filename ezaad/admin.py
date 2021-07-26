from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import   User

class UserAdmin(BaseUserAdmin):
    # list_display = ['username', 'is_staff', 'is_active']
    list_display = ['scim_username', 'is_staff', 'is_active']


admin.site.register(User, UserAdmin)