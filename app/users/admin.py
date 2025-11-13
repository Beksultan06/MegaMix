from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_active', 'is_manager', 'is_superuser')
    list_filter = ('is_manager', 'is_superuser', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Роли', {'fields': ('is_manager',)}),
    )