from django.test import TestCase
from datetime import datetime

from News.models import User, Author, Category, Post, Comment


class UserModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        User.objects.create_user(username='testuser',
                                 first_name='testuser_name',
                                 last_name='testuser_last_name',
                                 email='test@email.com',
                                 password='secret')

    def test_get_absolute_url(self):
        user = User.objects.get(id=1)
        self.assertEqual(user.get_absolute_url(), '/profile/')

    def test_object_name_is_first_name_comma_last_name(self):
        user = User.objects.get(id=1)
        self.assertEqual(f'{user.first_name} {user.last_name}', str(user))


class AuthorModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = User.objects.create_user(username='testuser',
                                        first_name='testuser_name',
                                        last_name='testuser_last_name',
                                        email='test@email.com',
                                        password='secret')
        Author.objects.create(user=user, user_rating=9)

    def test_user_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'Имя пользователя')

    def test_user_rating_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('user_rating').verbose_name
        self.assertEqual(field_label, 'Рейтинг пользователя')

    def test_object_name_is_user_object_name(self):
        author = Author.objects.get(id=1)
        user = author.user
        self.assertEqual(f'{user.first_name} {user.last_name}', str(user))

    def test_update_rating(self):
        pass  # TODO

    def test_user_rating_type_is_int(self):
        # TODO
        pass


class CategoryModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Category.objects.create(category_name='Politics')

    def test_category_name_content(self):
        content = Category.objects.get(id=1)
        self.assertEqual(content.category_name, 'Politics')

    def test_category_name_label(self):
        category = Category.objects.get(id=1)
        field_label = category._meta.get_field('category_name').verbose_name
        self.assertEqual(field_label, 'Название категории')

    def test_object_name_is_category_name_title(self):
        category = Category.objects.get(id=1)
        self.assertEqual(f'{category.category_name.title()}', str(category))

    def test_max_length_category_name_is_64(self):
        category = Category.objects.create(
            category_name='тескт для тестирования максимальной длины названия категории статьи')
        self.assertFalse(len(category.category_name) <= 64)


class PostModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = User.objects.create_user(username='testuser',
                                        first_name='testuser_name',
                                        last_name='testuser_last_name',
                                        email='test@email.com',
                                        password='secret')
        author = Author.objects.create(user=user)

        category = Category.objects.create(category_name='Политика')
        post = Post.objects.create(author=author,
                                   type='NE',
                                   date=datetime.now(),
                                   title='политика',
                                   text='someting text',
                                   )
        post.category.add(category)

    def test_author_name_label(self):
        post = Post.objects.get(id=1)
        field_label = post._meta.get_field('author').verbose_name
        self.assertEqual(field_label, 'Автор')

    def test_type_name_label(self):
        post = Post.objects.get(id=1)
        field_label = post._meta.get_field('type').verbose_name
        self.assertEqual(field_label, 'Тип')

    def test_date_name_label(self):
        post = Post.objects.get(id=1)
        field_label = post._meta.get_field('date').verbose_name
        self.assertEqual(field_label, 'Дата')

    def test_category_name_label(self):
        post = Post.objects.get(id=1)
        field_label = post._meta.get_field('category').verbose_name
        self.assertEqual(field_label, 'category')

    def test_title_name_label(self):
        post = Post.objects.get(id=1)
        field_label = post._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'Заголовок')

    def test_title_content(self):
        post = Post.objects.get(id=1)
        self.assertEqual(post.title, 'политика')

    def test_text_name_label(self):
        post = Post.objects.get(id=1)
        field_label = post._meta.get_field('text').verbose_name
        self.assertEqual(field_label, 'Текст')

    def test_text_content(self):
        post = Post.objects.get(id=1)
        self.assertEqual(post.text, 'someting text')

    def test_post_rating_name_label(self):
        post = Post.objects.get(id=1)
        field_label = post._meta.get_field('_post_rating').verbose_name
        self.assertEqual(field_label, 'Рейтинг')

    def test_object_name_is_post_author_comma_text_100_symbol(self):
        post = Post.objects.get(id=1)
        self.assertEqual(f'{post.author}: {post.text[:100]}', str(post))

    def test_increases_post_rating_on_1(self):
        post = Post.objects.get(id=1)
        post.post_rating = 0
        post.like()
        self.assertEqual(post.post_rating, 1)

    def test_reduce_post_rating_on_1(self):
        post = Post.objects.get(id=1)
        post.post_rating = 2
        post.dislike()
        self.assertEqual(post.post_rating, 1)

    def test_preview_metod_return_text_123_symb(self):
        post = Post.objects.get(id=1)
        self.assertEqual(f'{post.text[:123]} ...', post.preview())

    def test_get_absolute_url(self):
        post = Post.objects.get(id=1)
        self.assertEqual('/news/1/', post.get_absolute_url())


class CommentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = User.objects.create_user(username='testuser',
                                        first_name='testuser_name',
                                        last_name='testuser_last_name',
                                        email='test@email.com',
                                        password='secret')
        author = Author.objects.create(user=user)

        category = Category.objects.create(category_name='Политика')
        post = Post.objects.create(author=author,
                                   type='NE',
                                   date=datetime.now(),
                                   title='политика',
                                   text='someting text',
                                   )
        post.category.add(category)
        Comment.objects.create(post=post,
                               user=user,
                               comment_text='some comment',
                               comment_date=datetime.now(),
                               )

    def test_post_name_label(self):
        comment = Comment.objects.get(id=1)
        field_label = comment._meta.get_field('post').verbose_name
        self.assertEqual(field_label, 'Пост')

    def test_user_name_label(self):
        comment = Comment.objects.get(id=1)
        field_label = comment._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'Пользователь')

    def test_comment_text_name_label(self):
        comment = Comment.objects.get(id=1)
        field_label = comment._meta.get_field('comment_text').verbose_name
        self.assertEqual(field_label, 'Комментарии к посту')

    def test_comment_content(self):
        comment = Comment.objects.get(id=1)
        self.assertEqual(comment.comment_text, 'some comment')

    def test_comment_date_name_label(self):
        comment = Comment.objects.get(id=1)
        field_label = comment._meta.get_field('comment_date').verbose_name
        self.assertEqual(field_label, 'comment date')

    def test_comment_rating_name_label(self):
        comment = Comment.objects.get(id=1)
        field_label = comment._meta.get_field('_comment_rating').verbose_name
        self.assertEqual(field_label, 'Рейтинг комментария')

    def test_increases_comment_rating_on_1(self):
        comment = Comment.objects.get(id=1)
        comment.comment_rating = 0
        comment.like()
        self.assertEqual(comment.comment_rating, 1)

    def test_reduce_comment_rating_on_1(self):
        comment = Comment.objects.get(id=1)
        comment.comment_rating = 2
        comment.dislike()
        self.assertEqual(comment.comment_rating, 1)


class CategorySubcribesModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        # TODO
        pass
