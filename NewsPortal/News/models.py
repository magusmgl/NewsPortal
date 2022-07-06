from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

# Create your models here.
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_rating = models.FloatField(default=0.0)

    # def update_rating(self):
    #     pass


class Category(models.Model):
    category_name = models.CharField(max_length=64, unique=True)


class Post(models.Model):
    news = 'NE'
    blog = 'Bl'
    TYPE_ITEM = [
        (news, 'Новости'),
        (blog, 'Блог')
    ]

    post_author = models.ForeignKey('Author', on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2,
                                 choices=TYPE_ITEM,
                                 default=news)
    post_date = models.DateField(auto_now_add=True)
    post_category = models.ManyToManyField('Category', through='PostCategory')
    post_header = models.CharField(max_length=125)
    post_text = models.TextField()
    _post_rating = models.FloatField(default=0.0)

    @property
    def post_rating(self):
        return self._post_rating

    @post_rating.setter
    def post_rating(self, value):
        self._post_rating = value

    def like(self):
        self.post_rating += 1

    def dislike(self):
        self.post_rating -= 1

    def preview(self):
        return self.post_text[:125] + '...'


class PostCategory(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)
    _comment_rating = models.IntegerField(default=0)

    # @getattr
    # def comment_rating(self):
    #     return self._comment_rating
    #
    # @comment_rating.settr
    # def comment_rating(self, value):
    #     self._comment_rating = value
    #
    # def like(self):
    #     self.comment_rating += 1
    #
    # def dislike(self):
    #     self.comment_rating -= 1
