from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _


from .models import Feedback, Message
from .models import User


class UserPostsTabular(admin.TabularInline):
    from post.models import Posts
    model = Posts
    fields = ('title', 'create_date')
    extra = 0
    readonly_fields = fields

    def get_queryset(self, request):
        queryset = self.model.objects.all()
        return queryset

    def has_add_permission(self, request, obj):
        return False


class UsersTitleFilter(admin.SimpleListFilter):
    title = 'Users Filter'
    parameter_name = 'users_filter'

    def lookups(self, request, model_admin):
        users = User.objects.all()
        lst = [(user.username[0].title(), user.username[0].title()) for user in users]
        return tuple(sorted(set(lst)))

    def queryset(self, request, queryset):
        print(self.value())
        match self.value():
            case None:
                return User.objects.all()
            case _:
                return User.objects.filter(username__istartswith=str(self.value()[0]))


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

    readonly_fields = ('last_login', 'date_joined', 'avatar_img', )
    list_filter = (UsersTitleFilter,
                   ('is_activated', admin.BooleanFieldListFilter),
                   ('is_staff', admin.BooleanFieldListFilter)
                   )
    inlines = [UserPostsTabular, ]

    def avatar_img(self, obj):
        return format_html(f'<img src="{obj.avatar.url}" alt="{obj.username}" width="50" height="50">')


class MessagesFilter(admin.SimpleListFilter):
    title = 'Is read'
    parameter_name = 'is_read_filter'

    def lookups(self, request, model_admin):
        return (
            ('True', _('Read')),
            ('False', _('Unread')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'True':
            return Message.objects.filter(is_readed=True)
        if self.value() == 'False':
            return Message.objects.filter(is_readed=False)


class SenderFilter(admin.SimpleListFilter):
    title = 'sender'
    parameter_name = 'sender_name'

    def lookups(self, request, model_admin):
        messages = Message.objects.all()
        lst = [(message.sender, message.sender) for message in messages]
        return tuple(set(lst))

    def queryset(self, request, queryset):
        match self.value():
            case None:
                return Message.objects.all()
            case _:
                return Message.objects.filter(sender__username=self.value())


@admin.register(Message)
class AdminMessage(admin.ModelAdmin):
    list_display = ('name', 'subject', 'sender', 'recipient', 'is_readed',)
    readonly_fields = ('is_readed', )
    fieldsets = (
        ('Contacts', {'fields': (('sender', 'recipient',),)}),
        ('Subject', {'fields': ('subject', 'name')}),
        ('Subject', {'fields': ('body', )}),
        ('Status', {'fields': ('is_readed', )})
    )
    list_filter = (SenderFilter, MessagesFilter)


@admin.register(Feedback)
class AdminFeedBack(admin.ModelAdmin):
    list_display = ('email', 'ip_address', 'user')
    readonly_fields = ('time_create',)
    fieldsets = (
        ('Contacts', {'fields': (('email', 'user', 'ip_address',),)}),
        ('Subject', {'fields': ('subject', )}),
        ('Content', {'fields': ('content',)}),
        ('Create time', {'fields': ('time_create',)})
    )
