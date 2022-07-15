from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Sum


# Create your models here.
class User(AbstractUser):
    pass


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='author')
    user_rating = models.SmallIntegerField(default=0, db_column='rating')

    @staticmethod
    def update_rating(user):
        rating_posts_user = rating_comments_user = rating_comments_on_post_user = 0

        if user.author.posts.all().exists():
            rating_posts_user = user.author.posts.aggregate(rating=Sum('_post_rating'))['rating']

        if user.comments.all().exists():
            rating_comments_user = user.comments.aggregate(rating=Sum('_comment_rating'))['rating']

        if user.author.posts.all().exists():
            for post in user.author.posts.all():
                rating_comments_on_post_user += post.comments.aggregate(rating=Sum('_comment_rating'))['rating']

        user.author.user_rating = rating_posts_user * 3 + rating_comments_user + rating_comments_on_post_user
        user.author.save()


class Category(models.Model):
    category_name = models.CharField(max_length=64, unique=True, db_column='name')


class Post(models.Model):
    news = 'NE'
    article = 'AR'
    TYPE_ITEM = [
        (news, 'Новости'),
        (article, 'Статья')
    ]

    post_author = models.ForeignKey('Author',
                                    on_delete=models.CASCADE,
                                    db_column='author',
                                    related_name='posts')
    post_type = models.CharField(max_length=2,
                                 choices=TYPE_ITEM,
                                 default=news)
    post_date = models.DateField(auto_now_add=True, db_column='date')
    post_category = models.ManyToManyField('Category', through='PostCategory', db_column='category')
    post_title = models.CharField(default='', max_length=128, db_column='header')
    post_text = models.TextField(db_column='text')
    _post_rating = models.SmallIntegerField(default=0, db_column='rating')

    @property
    def post_rating(self):
        return self._post_rating

    @post_rating.setter
    def post_rating(self, value):
        self._post_rating = value
        self.save()

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        return f'{self.post_text[:123]} ...'


class PostCategory(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='comments')
    comment_text = models.TextField(db_column='text')
    comment_date = models.DateTimeField(auto_now_add=True, db_column='date')
    _comment_rating = models.IntegerField(default=0, db_column='rating')

    @property
    def comment_rating(self):
        return self._comment_rating

    @comment_rating.setter
    def comment_rating(self, value):
        self._comment_rating = value
        self.save()

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()
