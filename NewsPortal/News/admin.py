from django.core.paginator import Paginator
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from modeltranslation.admin import TranslationAdmin

from .models import (
    User,
    Post,
    Category,
    Author,
    Comment,
    PostCategory,
    CategorySubcribes,
)


# Register your models here.
class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


class PostInline(admin.TabularInline):
    model = Post
    fk_name = 'author'
    extra = 0


class CategoryPostInline(admin.StackedInline):
    model = PostCategory
    fk_name = 'post'
    extra = 0


class CategorySubscribesInline(admin.StackedInline):
    model = CategorySubcribes
    fk_name = 'subcribe_user'
    extra = 0


class SubscribersInline(admin.StackedInline):
    model = Category.subscribers.through
    extra = 0


def nullfy_commets_rating(modeladmin, request, queryset):
    queryset.update(_comment_rating=0)


nullfy_commets_rating.short_description = 'Обнулить рейтинг комментариев'


def nullfy_posts_rating(modeladmin, request, queryset):
    queryset.update(_comment_rating=0)


nullfy_posts_rating.short_description = 'Обнулить рейтинг постов'


@admin.register(Comment)
class CommentAdmin(TranslationAdmin):
    list_display = [field.name for field in Comment._meta.get_fields()]
    list_filter = ('user', 'comment_date',)
    search_fields = ['comment_text']
    actions = [nullfy_commets_rating]
    ordering = ['post']


@admin.register(Post)
class PostAdmin(TranslationAdmin):
    inlines = [
        CategoryPostInline,
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
    paginator = Paginator
    list_per_page = 10
    ordering = ['date']


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    inlines = [
        PostInline,
    ]
    list_display = ('user', 'user_rating')
    list_filter = ('user',)


admin.site.register(User, UserAdmin)


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    model = Category
    inlines = [
        SubscribersInline,
    ]
    exclude = ('subscribers',)
    list_display = ('category_name', 'number_of_subscribers')
