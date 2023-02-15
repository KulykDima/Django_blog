from django.contrib import admin

from post.models import Comment
from post.models import Posts


class CommentsTabularInline(admin.TabularInline):
    from .models import Comment
    model = Comment
    fields = ('user', 'created', )
    extra = 0
    readonly_fields = fields

    def get_queryset(self, request):
        queryset = self.model.objects.select_related('user')
        return queryset

    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class PostsFilter(admin.SimpleListFilter):
    title = 'Posts Filter'
    parameter_name = 'posts_filter'

    def lookups(self, request, model_admin):
        posts = Posts.objects.all()
        lst = [(post.title[0], post.title[0]) for post in posts]
        return tuple(sorted(set(lst)))

    def queryset(self, request, queryset):
        print(self.value())
        match self.value():
            case None:
                return Posts.objects.all()
            case _:
                return Posts.objects.filter(title__istartswith=str(self.value()[0]))


@admin.register(Posts)
class AdminPost(admin.ModelAdmin):
    list_display = ('title', 'author', 'create_date', )
    fieldsets = (
        ('Author info', {'fields': (('author', 'create_date',),)}),
        ('Post info', {'fields': ('title', 'text')}),
        ('Likes and Dislikes', {'fields': (('like', 'dislike'), )}),
    )

    readonly_fields = ('create_date', 'like', 'dislike', )
    list_filter = (PostsFilter, )
    inlines = [CommentsTabularInline, ]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('post', 'body')
    fieldsets = (
        ('User info', {'fields': (('user', 'created', 'updated', ),)}),
        ('Post Comment', {'fields': ('post', 'body', )}),
        ('Active', {'fields': (('active', ), )}),
    )
    readonly_fields = ('created', 'updated', )
