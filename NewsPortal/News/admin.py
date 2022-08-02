from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Post, Category, Author

admin.site.register(User, UserAdmin)
admin.site.register(Author)
admin.site.register(Post)
admin.site.register(Category)