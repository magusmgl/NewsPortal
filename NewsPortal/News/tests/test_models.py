from django.test import TestCase
from datetime import datetime

from News.models import User, Author, Category, Post


class UserModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        User.objects.create_user(username='ivan1234',
                                 first_name='ivan',
                                 last_name='ivianov',
                                 email="ivan1234@mail.ru",
                                 password="1234")

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
        user = User.objects.create_user(username='ivan1234', first_name='ivan',
                                        last_name='ivianov',
                                        email="ivan1234@mail.ru",
                                        password="1234")
        Author.objects.create(user=user, user_rating=9.1231)

    def test_user_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'Пользователь')

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
        Category.objects.create(category_name='Политика')

    def test_category_name_label(self):
        category = Category.objects.get(id=1)
        field_label = category._meta.get_field('category_name').verbose_name
        self.assertEqual(field_label, 'Имя категории')

    def test_object_name_is_category_name_title(self):
        category = Category.objects.get(id=1)
        self.assertEqual(f'{category.category_name.title()}', str(category))

    def test_max_length_category_name_is_64(self):
        category = Category.objects.create(
            category_name='тескт для тестирования максимальной длины названия категории статьи')
        self.assertFalse(len(category.category_name) <= 64)


class POstModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = User.objects.create_user(username='ivan1234', first_name='ivan',
                                        last_name='ivianov',
                                        email="ivan1234@mail.ru",
                                        password="1234")
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
        self.assertEqual(field_label, 'Категория')

    def test_title_name_label(self):
        post = Post.objects.get(id=1)
        field_label = post._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'Заголовок')

    def test_text_name_label(self):
        post = Post.objects.get(id=1)
        field_label = post._meta.get_field('text').verbose_name
        self.assertEqual(field_label, 'Текст поста')

    def test_post_rating_name_label(self):
        post = Post.objects.get(id=1)
        field_label = post._meta.get_field('_post_rating').verbose_name
        self.assertEqual(field_label, 'Рейтинг поста')

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




