"""NewsPortal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from .views import NewsList, NewsDetail, NewsSearch, NewsCreate, NewsEdit, NewsDelete, ArticleCreate, EditProfile

urlpatterns = [
    path('news/', NewsList.as_view(), name='news_list'),
    path('news/<int:id>', NewsDetail.as_view(), name='news'),
    path('news/search', NewsSearch.as_view(), name='news_search'),
    path('news/create', NewsCreate.as_view(), name='news_create'),
    path('news/<int:pk>/edit', NewsEdit.as_view(), name='news_update'),
    path('news/<int:pk>/delete', NewsDelete.as_view(), name='news_delete'),
    path('artcle/create', ArticleCreate.as_view(), name='atricle_create'),
    path('article/<int:pk>/edit', NewsEdit.as_view(), name='news_update'),
    path('article/<int:pk>/delete', NewsDelete.as_view(), name='news_delete'),
    path('profile/<int:pk>/edit', EditProfile.as_view(), name='profile_edit'),
]
