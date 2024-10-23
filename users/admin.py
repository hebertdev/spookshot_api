"""User models admin."""

# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Models
from users.models import User, Profile


class CustomUserAdmin(UserAdmin):
    """User model admin."""
    list_display = ('email', 'username', 'first_name',
                    'last_name', 'is_staff', )

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Profile model admin."""
    list_display = ('user',)

admin.site.register(User, CustomUserAdmin)