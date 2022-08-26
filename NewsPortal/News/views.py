from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.cache import cache

from .models import Post, User, CategorySubcribes, Category
from .filters import NewsFilter
from .forms import PostForm, ArticleForm, ProfileForm
from .tasks import mailing_subscribers_after_news_creation


# Create your views here.
class NewsList(ListView):
    '''Представления для вывода списка новостей'''
    model = Post
    ordering = '-date'
    template_name = 'news/news_list.html'
    context_object_name = 'news_list'
    paginate_by = 10


class NewsDetail(DetailView):
    '''Представления для вывода конкретной новости'''
    model = Post
    template_name = 'news/news.html'
    context_object_name = 'news'
    pk_url_kwarg = 'id'

    def get_object(self, *args, **kwargs) -> None:
        '''
        Получение новости из кэша. Если новости в кэше нет, получаем новость из базы и затем сохраняем ее в кэш.
        '''
        news = cache.get(f'news-{self.kwargs["id"]}', None)
        if not news:
            news = super().get_object(queryset=self.queryset)
            cache.set(f'news-{self.kwargs["id"]}', news)
        return news


class NewsSearch(ListView):
    '''Представления для фильтрации новостей на сайте'''
    model = Post
    ordering = '-date'
    template_name = 'news/news_search.html'
    context_object_name = 'news_list'
    paginate_by = 10

    def get_queryset(self):
        '''Возвращает отфильтрованный запрос'''
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        '''Сохранение отфильтрованного запроса в context'''
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsCreate(PermissionRequiredMixin, CreateView):
    '''Представления для создания новостей для авторизованных пользователей'''
    permission_required = ('News.add_post')
    form_class = PostForm
    model = Post
    template_name = 'news/news_edit.html'

    def form_valid(self, form):
        '''При валидации формы сохраняем тип поста: новость'''
        news = form.save(commit=False)
        news.type = 'NE'
        news.save()
        mailing_subscribers_after_news_creation.delay(post_pk=news.pk)
        return super().form_valid(form)


class NewsEdit(PermissionRequiredMixin, UpdateView):
    '''Представление для редактирования новости'''
    permission_required = ('News.change_post')
    form_class = PostForm
    model = Post
    template_name = 'news/news_edit.html'


class NewsDelete(PermissionRequiredMixin, DeleteView):
    '''Удаление поста'''
    permission_required = ('News.delete_post')
    model = Post
    template_name = 'news/news_delete.html'
    success_url = reverse_lazy('news_list')


class ArticleCreate(PermissionRequiredMixin, CreateView):
    '''Представления для создания статьи для авторизованных пользователей'''
    permission_required = ('News.add_post')
    form_class = ArticleForm
    model = Post
    template_name = 'news/news_edit.html'

    def form_valid(self, form):
        '''При валидации формы сохраняем тип поста: статья'''
        news = form.save(commit=False)
        news.type = 'AR'
        return super().form_valid(form)


class ProfileDetail(LoginRequiredMixin, DetailView):
    '''Профиль пользователя'''
    template_name = 'news/profile.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        '''Получаем данные пользователя по pk'''
        return get_object_or_404(User, pk=self.request.user.pk)

    def get_context_data(self, **kwargs):
        '''Сохраняем к контексте информацию является ли пользователь автором'''
        context = super(ProfileDetail, self).get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class EditProfile(LoginRequiredMixin, UpdateView):
    '''Редактирования профиля пользователя'''
    form_class = ProfileForm
    template_name = 'news/profile_edit.html'

    def get_object(self, queryset=None):
        '''Получаем данные пользователя по pk'''
        return get_object_or_404(User, pk=self.request.user.pk)


@login_required()
def make_author(request):
    '''Добавляет юзера в группу авторов'''
    user = request.user
    author_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        author_group.user_set.add(user)
    return redirect('/profile/')


@login_required()
def subscribe_to_news_category(request, post_id):
    '''Подписка  пользователя на категории текущей новости'''
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
