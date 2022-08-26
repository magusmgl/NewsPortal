# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Sum
from django.core.cache import cache
from django.urls import reverse


class User(AbstractUser):
    '''Модель юзера наследуемая от AbstractUser'''

    def __str__(self):
        return self.get_full_name()

    def get_absolute_url(self) -> str:
        '''Получение абсолютного адреса профиля юзера'''
        return reverse('profile')

    class Meta:
        '''Добавлене названия таблиц в админке'''
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Author(models.Model):
    '''Модель автора поста/новости на сайте'''
    user = models.OneToOneField(to=User,
                                on_delete=models.CASCADE,
                                related_name='author',
                                verbose_name='Пользователь')
    user_rating = models.SmallIntegerField(default=0,
                                           db_column='rating',
                                           verbose_name='Рейтинг пользователя')

    def __str__(self) -> None:
        '''Возвращает полное имя юзера на сайте (имя, фамилия)'''
        return User.get_full_name(self.user)

    class Meta:
        '''Добавлене названия таблиц в админке'''
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    @staticmethod
    def update_rating(user) -> None:
        '''
        Обновляет и сохраняет рейтинг автора на сайте.
        Общий рейтинг считается исходя из рейтинга постов автра,
        рейтинга комментариев юзера и рейтига комментариев под постом автора.
         '''
        rating_posts_user = rating_comments_user = rating_comments_on_post_user = 0

        if user.author.posts.all().exists():
            rating_posts_user = user.author.posts.aggregate(rating=Sum('_post_rating'))['rating']

        if user.comments.all().exists():
            rating_comments_user = user.comments.aggregate(rating=Sum('_comment_rating'))['rating']

        if user.author.posts.all().exists():
            for post in user.author.posts.all():
                rating_comments_on_post_user += post.comments.aggregate(
                    rating=Sum('_comment_rating'))['rating']

        user.author.user_rating = rating_posts_user * 3 \
                                  + rating_comments_user \
                                  + rating_comments_on_post_user
        user.author.save()


class Category(models.Model):
    '''Модель описывает категории статьей на сайте и их подписчиков (юзеров)'''
    category_name = models.CharField(max_length=64,
                                     unique=True,
                                     db_column='name',
                                     verbose_name='Имя категории')
    subscribers = models.ManyToManyField(to='User',
                                         through='CategorySubcribes',
                                         db_column='category', )

    @property
    def __str__(self):
        '''Возвращает заголок поста/новости'''
        return f'{self.category_name.title()}.'

    class Meta:
        '''
        Добавление названия таблиц в админке и
        сортировка категорий по имени.
        '''
        verbose_name = 'Автор'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['category_name']


class Post(models.Model):
    '''Модель описывает посто на сайет (новость или статья)'''
    news = 'NE'
    article = 'AR'
    TYPE_ITEM = [
        (news, 'Новости'),
        (article, 'Статья')
    ]

    author = models.ForeignKey(to='Author',
                               on_delete=models.CASCADE,
                               db_column='author',
                               related_name='posts',
                               verbose_name='Автор')
    type = models.CharField(max_length=2,
                            choices=TYPE_ITEM,
                            default=news,
                            verbose_name='Тип')
    date = models.DateField(auto_now_add=True,
                            db_column='date',
                            verbose_name='Дата')
    category = models.ManyToManyField(to='Category',
                                      through='PostCategory',
                                      db_column='category',
                                      verbose_name='Категория')
    title = models.CharField(default='',
                             max_length=128,
                             db_column='header',
                             verbose_name='Заголовок')
    text = models.TextField(db_column='text', verbose_name='Текст поста')
    _post_rating = models.SmallIntegerField(default=0,
                                            db_column='rating',
                                            verbose_name='Рейтинг поста')

    class Meta:
        '''
        Добавление названия таблиц в админке и
        сортировка постов по дате добавленя.
        '''
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['date']

    def __str__(self) -> str:
        '''Выводит автора статьи и первые 100 знаков статьи'''
        return f'{self.author}: {self.text[:100]}'

    @property
    def post_rating(self):
        '''Получение рейтинга поста'''
        return self._post_rating

    @post_rating.setter
    def post_rating(self, value):
        self._post_rating = value
        self.save()

    def like(self) -> None:
        '''Увеличивает рейтинг статьи на 1'''
        self.post_rating += 1
        self.save()

    def dislike(self):
        '''Уменьшает рейтинг статьи на 1'''
        self.post_rating -= 1
        self.save()

    def preview(self):
        '''Выводит превью статьи, первые 123 знака'''
        return f'{self.text[:123]} ...'

    def get_absolute_url(self) -> str:
        '''Получене абсолютной ссылки на кокрентую статью'''

        return reverse('news', kwargs={'id': self.pk})

    def save(self, *args, **kwargs):
        '''
        Переопределяет стандарнты метод save.
        Удаляет данные статьи из кэша, после ее сохранения/изменения.
        '''
        super().save(*args, **kwargs)
        cache.delete(f'news-{self.pk}')


class PostCategory(models.Model):
    '''Промежуточная модель связывающая таблицы Post и Category'''
    post = models.ForeignKey(to='Post', on_delete=models.CASCADE)
    category = models.ForeignKey(to='Category', on_delete=models.CASCADE)


class Comment(models.Model):
    '''Модель комментариев поста'''
    post = models.ForeignKey(to='Post', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(to='User', on_delete=models.CASCADE, related_name='comments')
    comment_text = models.TextField(db_column='text')
    comment_date = models.DateTimeField(auto_now_add=True, db_column='date')
    _comment_rating = models.IntegerField(default=0, db_column='rating')

    @property
    def comment_rating(self):
        '''Получение рейтинга комментария'''
        return self._comment_rating

    @comment_rating.setter
    def comment_rating(self, value):
        self._comment_rating = value
        self.save()

    def like(self):
        '''Увеличивает рейтинг комментария на 1'''
        self.comment_rating += 1
        self.save()

    def dislike(self):
        '''Уменьшает рейтинг комментария на 1'''
        self.comment_rating -= 1
        self.save()


class CategorySubcribes(models.Model):
    """ Модель ПОДПИСКИ на КАТЕОРИЮ """
    subcribe_user = models.ForeignKey(to='User',
                                      null=True,
                                      on_delete=models.SET_NULL,
                                      verbose_name='Подписчик')
    category = models.ForeignKey(to='Category',
                                 null=True,
                                 on_delete=models.SET_NULL,
                                 verbose_name='Категория')
