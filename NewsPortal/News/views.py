from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .models import Post, User, CategorySubcribes, Category
from .filters import NewsFilter
from .forms import PostForm, ArticleForm, ProfileForm
from .tasks import mailing_subscribers_after_news_creation


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


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('News.add_post')
    form_class = PostForm
    model = Post
    template_name = 'news/news_edit.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.type = 'NE'
        news.save()
        mailing_subscribers_after_news_creation.delay(post_pk=news.pk)
        return super().form_valid(form)


class NewsEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('News.change_post')
    form_class = PostForm
    model = Post
    template_name = 'news/news_edit.html'


class NewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('News.delete_post')
    model = Post
    template_name = 'news/news_delete.html'
    success_url = reverse_lazy('news_list')


class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('News.add_post')
    form_class = ArticleForm
    model = Post
    template_name = 'news/news_edit.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.type = 'AR'
        return super().form_valid(form)


class ProfileDetail(LoginRequiredMixin, DetailView):
    template_name = 'news/profile.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return get_object_or_404(User, pk=self.request.user.pk)

    def get_context_data(self, **kwargs):
        context = super(ProfileDetail, self).get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class EditProfile(LoginRequiredMixin, UpdateView):
    form_class = ProfileForm
    template_name = 'news/profile_edit.html'

    def get_object(self, queryset=None):
        return get_object_or_404(User, pk=self.request.user.pk)


@login_required()
def make_author(request):
    user = request.user
    author_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        author_group.user_set.add(user)
    return redirect('/profile/')


@login_required()
def subscribe_to_news_category(request, post_id):
    '''Подписка  пользователя на категории текущей новости и отправка сообщения'''
    user = request.user
    post_categories = Category.objects.filter(post=post_id)
    for category in post_categories:
        if not user.categorysubcribes_set.filter(category=category).exists():
            CategorySubcribes.objects.create(subcribe_user=user, category=category)

    context = {
        'post_id': post_id,
        'user': user,
        'categories_subscribed': user.category_set.all(),
    }

    return render(request, 'news/subcribe.html', context=context)
