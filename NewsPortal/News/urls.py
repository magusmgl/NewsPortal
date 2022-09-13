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
from django.urls import path

from .views import (
    NewsList,
    NewsDetail,
    NewsSearch,
    NewsCreate,
    NewsEdit,
    NewsDelete,
    ArticleCreate,
    EditProfile,
    ProfileDetail,
    make_author,
    subscribe_to_news_category
)
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('profile/', ProfileDetail.as_view(), name='profile'),
    path('profile/edit/', EditProfile.as_view(), name='profile_edit'),
    path('profile/upgrade/', make_author, name='make_author'),
    path('search/', NewsSearch.as_view(), name='news_search'),
    path('create/', NewsCreate.as_view(), name='news_create'),
    path('<int:id>/', NewsDetail.as_view(), name='news_detail'),
    path('<int:post_id>/subscribe', subscribe_to_news_category, name='news_subscribe'),
    path('<int:pk>/edit/', NewsEdit.as_view(), name='news_update'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('', NewsList.as_view(), name='news_list'),
]
