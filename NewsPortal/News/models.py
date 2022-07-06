from django.db import models


# Create your models here.
class Author(models.Model):
    user = models.OneToOneField(on_delete=models.CASCADE)
    user_rating = models.FloatField()

    def update_rating(self):
        pass



class Category(models.Model):
    category_name = models.CharField(max_length=64, unique=True)


class Post(models.Model):
    post_author = models.ForeignKey()
    post_type = models.ChoiceField()
    post_date = models.DateField(auto_now_add=True)
    post_category = models.ManyToManyField()
    post_header = models.CharField(max_length=125)
    post_text = models.TextField()
    _post_raing = models.IntegerField(default=0)

    @getattr
    def post_rating(self):
        return self._post_raing

    @post_rating.settr
    def post_rating(self, value):
        self._post_raing = value


    def like(self):
        self.post_rating += 1

    def dislike(self):
        self.post_rating -= 1

    def preview(self):
        return self.post_text[:125] + '...'


class PostCategory(models.Model):
    pass
    # post
    # category


class Comment(models.Model):
    post = models.ForeignKey()
    user = models.ForeignKey()
    comment_text = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)
    _comment_rating = models.IntegerField(default=0)

    @getattr
    def comment_rating(self):
        return self._comment_rating

    @comment_rating.settr
    def comment_rating(self, value):
        self._comment_rating = value

    def like(self):
        self.comment_rating += 1

    def dislike(self):
        self.comment_rating -= 1
