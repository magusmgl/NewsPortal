from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Sum


# Create your models here.
class User(AbstractUser):
    pass


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='author')
    user_rating = models.FloatField(default=0.0, db_column='rating')

    @staticmethod
    def update_rating(user):
        rating_post_author = rating_comment_author = rating_comment_for_post_author = 0

        if user.author.posts.exists():
            rating_post_author = user.author.posts.aggregate(rating=Sum('_post_rating'))['rating']

        if user.comments.exists():
            rating_comment_author = user.comments.aggregate(rating=Sum('_comment_rating'))['rating']

        if user.author.posts.exists():
            for post in user.author.posts.all():
                rating_comment_for_post_author += post.comments.aggregate(rating=Sum('_comment_rating'))['rating']

        user.author.user_rating = rating_post_author * 3 + rating_comment_author + rating_comment_for_post_author
        user.author.save()


class Category(models.Model):
    category_name = models.CharField(max_length=64, unique=True, db_column='name')


class Post(models.Model):
    news = 'NE'
    blog = 'Bl'
    TYPE_ITEM = [
        (news, 'Новости'),
        (blog, 'Блог')
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
    post_header = models.CharField(max_length=125, db_column='header')
    post_text = models.TextField(db_column='text')
    _post_rating = models.IntegerField(default=0, db_column='rating')

    @property
    def post_rating(self):
        return self._post_rating

    @post_rating.setter
    def post_rating(self, value):
        self._post_rating = value

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        return self.post_text[:125] + ' ...'


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

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()
