from django.contrib import admin
from django.utils.html import format_html

from .models import User


class StaffFilter(admin.SimpleListFilter):
    title = 'Staff Filter'
    parameter_name = 'staff_filter'

    def lookups(self, request, model_admin):
        users = User.objects.all()
        lst = [(user.is_staff, user.is_staff) for user in users]
        return tuple(sorted(set(lst)))

    def queryset(self, request, queryset):
        match self.value():
            case None:
                return User.objects.all()
            case _:
                return User.objects.filter(is_staff=str(self.value()))


class ActivatedFilter(admin.SimpleListFilter):
    title = 'Activated Filter'
    parameter_name = 'activated_filter'

    def lookups(self, request, model_admin):
        users = User.objects.all()
        lst = [(user.is_activated, user.is_activated) for user in users]
        return tuple(sorted(set(lst)))

    def queryset(self, request, queryset):
        print(self.value())
        match self.value():
            case None:
                return User.objects.all()
            case _:
                return User.objects.filter(is_activated=str(self.value()))


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
    list_filter = (ActivatedFilter, StaffFilter, )

    def avatar_img(self, obj):
        return format_html(f'<img src="{obj.avatar.url}" alt="{obj.username}" width="50" height="50">')
