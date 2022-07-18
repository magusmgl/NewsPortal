from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post


# Create your views here.
class NewsList(ListView):
    # model = Post
    # ordering = 'post_date'
    queryset = Post.objects.order_by('-date')
    template_name = 'news_list.html'
    context_object_name = 'news_list'


class NewsDetail(DetailView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    pk_url_kwarg = 'id'
