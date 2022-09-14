from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    User,
    Post,
    Category,
    Author,
    Comment,
)


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


def nullfy_commets_rating(modeladmin, request, queryset):
    queryset.update(_comment_rating=0)


nullfy_commets_rating.short_description = 'Обнулить рейтинг комментариев'


def nullfy_posts_rating(modeladmin, request, queryset):
    queryset.update(_comment_rating=0)


nullfy_posts_rating.short_description = 'Обнулить рейтинг постов'


class CommentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Comment._meta.get_fields()]
    list_filter = ('user', 'comment_date',)
    search_fields = ['comment_text']
    actions = [nullfy_commets_rating]


class PostAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline,
    ]
    list_display = (
        'author',
        'type',
        'date',
        'title',
        'text',
        '_post_rating',
    )
    list_filter = ('author', 'type', 'date',)
    search_fields = ['title__icontains']
    actions = [nullfy_posts_rating]


admin.site.register(User, UserAdmin)
admin.site.register(Author)
admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Comment, CommentAdmin)
