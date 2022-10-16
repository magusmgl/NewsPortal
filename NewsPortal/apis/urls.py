from django.contrib import admin
from django.urls import path, include

from .views import (
    AuthorsApiViews,
    AuthorDetailApiViews,
    PostsAuthorApiViews,
    PostsApiViews,
    PostDeatailApiViews,
    PostEditApiViews,
    PostDeleteApiViews,
)

urlpatterns = [
    path('authors/', AuthorsApiViews, name='author_list'),
    path('authors/<int:pk>/', AuthorDetailApiViews, name='author_detail'),
    path('authors/<int:author_pk>/posts/', PostsAuthorApiViews, name='author_posts'),
    path('posts/', PostsApiViews, name='post_list'),
    path('posts/<int:pk>/', PostDeatailApiViews, name='post_detail'),
    path('posts/<int:pk>/edit/', PostEditApiViews, name='post_edit'),
    path('posts/<int:pk>/delete/', PostDeleteApiViews, name='post_delete')

]
