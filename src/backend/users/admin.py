from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'credits', 'materials_count', 'downloads_count', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('扩展信息', {
            'fields': ('avatar', 'bio', 'website', 'credits', 'materials_count', 'downloads_count')
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('扩展信息', {
            'fields': ('avatar', 'bio', 'website', 'credits')
        }),
    )