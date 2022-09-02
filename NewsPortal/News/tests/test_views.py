from datetime import datetime

from django.test import TestCase, SimpleTestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from News.models import User, Author, Category, Post


class NewsListTests(TestCase):

    def test_url_exists_at_correct_loction(self):
        response = self.client.get('/news/')
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        response = self.client.get(reverse('news_list'))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(reverse('news_list'))
        self.assertTemplateUsed(response, 'news/news_list.html')


class NewsDetailTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username='testuser',
                                                        first_name='testuser_name',
                                                        last_name='testuser_last_name',
                                                        email='test@email.com',
                                                        password='secret')

        cls.author = Author.objects.create(user=cls.user)

        cls.category = Category.objects.create(category_name='Политика')
        cls.post = Post.objects.create(author=cls.author,
                                       type='NE',
                                       date=datetime.now(),
                                       title='политика',
                                       text='someting text',
                                       )
        cls.post.category.add(cls.category)

    def test_url_exists_at_correct_location_detailview(self):
        response = self.client.get('/news/1/')
        self.assertEqual(response.status_code, 200)

    def test_post_detailview(self):
        response = self.client.get(reverse('news',
                                           kwargs={'id': self.post.id}))
        no_response = self.client.get('/news/100000/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertTemplateUsed(response, 'news/news.html')


class NewsSearchTest(TestCase):

    def test_url_exists_at_correct_loction(self):
        respounce = self.client.get('/news/search/')
        self.assertEqual(respounce.status_code, 200)

    def test_url_available_by_name(self):
        response = self.client.get(reverse('news_search'))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(reverse('news_search'))
        self.assertTemplateUsed(response, 'news/news_search.html')
