from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Post, User
from .filters import NewsFilter
from .forms import PostForm, ArticleForm, ProfileForm


# Create your views here.
class NewsList(ListView):
    model = Post
    ordering = '-date'
    template_name = 'news/news_list.html'
    context_object_name = 'news_list'
    paginate_by = 10


class NewsDetail(DetailView):
    model = Post
    template_name = 'news/news.html'
    context_object_name = 'news'
    pk_url_kwarg = 'id'


class NewsSearch(ListView):
    model = Post
    ordering = '-date'
    template_name = 'news/news_search.html'
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


class NewsCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news/news_edit.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.type = 'NE'
        return super().form_valid(form)


class NewsEdit(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news/news_edit.html'


class NewsDelete(DeleteView):
    model = Post
    template_name = 'news/news_delete.html'
    success_url = reverse_lazy('news_list')


class ArticleCreate(CreateView):
    form_class = ArticleForm
    model = Post
    template_name = 'news/news_edit.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.type = 'AR'
        return super().form_valid(form)

class EditProfile(LoginRequiredMixin, UpdateView):
    form_class = ProfileForm
    model = User
    template_name = 'news/profile_edit.html'