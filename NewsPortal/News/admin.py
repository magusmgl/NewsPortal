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


class PostAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline,
    ]


admin.site.register(User, UserAdmin)
admin.site.register(Author)
admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Comment)
