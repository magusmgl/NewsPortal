from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from News.forms import PostForm, User, Author, Category
from News.models import User, Author, Category, Post


class PostFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username='testuser',
                                                        first_name='testuser_name',
                                                        last_name='testuser_last_name',
                                                        email='test@email.com',
                                                        password='secret')

        cls.author = Author.objects.create(user=cls.user)
        cls.category = Category.objects.create(category_name='Политика')

    def test_post_form_author_label(self):
        form = PostForm()
        self.assertTrue(form.fields['author'].label == None or form.fields['author'].label == 'Автор поста')

    def test_post_form_author_empty_label(self):
        form = PostForm()
        self.assertTrue(form.fields['author'].empty_label == '-- Выберите автора --')

    def test_post_form_category_label(self):
        form = PostForm()
        self.assertTrue(form.fields['category'].label == None or form.fields['category'].label == 'Категория поста')

    def test_post_form_title_label(self):
        form = PostForm()
        self.assertTrue(form.fields['title'].label == None or form.fields['title'].label == 'Заголовок поста')

    def test_post_form_text_label(self):
        form = PostForm()
        self.assertTrue(form.fields['text'].label == None or form.fields['text'].label == 'Текст поста')

    def test_post_form_text_equal_to_title(self):
        user = User.objects.create_user(username='ivan1234', first_name='ivan', last_name='ivianov',
                                        email="ivan1234@mail.ru", password="1234")
        author = Author.objects.create(user=user)
        category = Category.objects.create(category_name='Политика')
        title = '_' * 150
        text = '_' * 150

        form_data = {'category': [category], 'author': author, 'title': title, 'text': text, }
        form = PostForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_post_form_text_not_equal_to_title(self):
        user = User.objects.create_user(username='ivan1234', first_name='ivan', last_name='ivianov',
                                        email="ivan1234@mail.ru", password="1234")
        author = Author.objects.create(user=user)
        category = Category.objects.create(category_name='Политика')
        title = '_' * 15
        text = '_' * 200

        form_data = {'category': [category], 'author': author, 'title': title, 'text': text, }
        form = PostForm(data=form_data)
        self.assertTrue(form.is_valid())

    # def test_news_create(self):
    #     response = self.client.post(
    #         reverse('news_create'),
    #         {
    #             'author': self.author,
    #             'category': self.category,
    #             'title': 'New title',
    #             'text': 'New text',
    #         }
    #     )
    #     self.assertEqual(response.status_code, 302)
    #     self.assertEqual(Post.objects.last().title, 'New title')
    #     self.assertEqual(Post.objects.last().text, 'New text')
    #
    # def test_news_edit(self):
    #     response = self.client.post(
    #         reverse('news_update', args=1),
    #         {
    #             'title': 'Update title',
    #             'text': 'Body text',
    #         })
