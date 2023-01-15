from django.contrib import admin
from django.utils.html import format_html

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'is_superuser', 'is_staff', 'is_active', 'is_activated', )
    fieldsets = (
        ('Image', {'fields': (('avatar', 'avatar_img',), )}),
        ('Register info', {'fields': ('username', 'email')}),
        ('Personal info', {'fields': (('last_name', 'first_name'), ('birthday', 'city'))}),
        ('Permission', {'fields': ('groups', 'user_permissions')}),
        ('Flags', {'fields': (('is_superuser', 'is_staff', 'is_active', 'is_activated'), )}),
        ('Login info', {'fields': (('last_login', 'date_joined'), )})
    )

    readonly_fields = ('last_login', 'date_joined', 'avatar_img')

    def avatar_img(self, obj):
        return format_html(f'<img src="{obj.avatar.url}" alt="{obj.username}" width="50" height="50">')
