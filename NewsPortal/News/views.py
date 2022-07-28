from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post
from .filters import NewsFilter


# Create your views here.
class NewsList(ListView):
    model = Post
    ordering = '-date'
    template_name = 'news_list.html'
    context_object_name = 'news_list'
    paginate_by = 10


class NewsDetail(DetailView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    pk_url_kwarg = 'id'


class NewsSearch(ListView):
    model = Post
    ordering = '-date'
    template_name = 'news_search.html'
    context_object_name = 'news_list'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context
