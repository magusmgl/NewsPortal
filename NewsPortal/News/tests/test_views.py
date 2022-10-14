from datetime import datetime

from django.test import TestCase, SimpleTestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from News.models import User, Author, Category, Post


class NewsListTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username='testuser',
                                                        first_name='testuser_name',
                                                        last_name='testuser_last_name',
                                                        email='test@email.com',
                                                        password='secret')

        cls.author = Author.objects.create(user=cls.user)

        cls.category = Category.objects.create(category_name='Политика')
        number_posts = 33
        for post_num in range(number_posts):
            Post.objects.create(author=cls.author,
                                type='NE',
                                date=datetime.now(),
                                title=f'some titlte {post_num}',
                                text=f'someting text {post_num}',
                                )

    def test_view_url_exists_at_correct_loction(self):
        response = self.client.get('/news/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_available_by_name(self):
        response = self.client.get(reverse('news_list'))
        self.assertEqual(response.status_code, 200)

    def test_view_template_name_correct(self):
        response = self.client.get(reverse('news_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news/news_list.html')

    def test_pagination_is_ten(self):
        response = self.client.get(reverse('news_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['object_list']) == 10)

    def test_lists_all_post(self):
        # Переходим на 4 страницу новостей и проверяем что на ней выводится только 3 новости
        response = self.client.get(reverse('news_list') + '?page=4')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['object_list']) == 3)


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
                                       title='some title',
                                       text='some text',
                                       )
        cls.post.category.add(cls.category)

    def test_url_exists_at_correct_location_detailview(self):
        response = self.client.get('/news/1/')
        self.assertEqual(response.status_code, 200)

    def test_post_detailview(self):
        response = self.client.get(reverse('news_detail',
                                           kwargs={'id': self.post.id}))
        no_response = self.client.get('/news/100000/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertTemplateUsed(response, 'news/news_detail.html')


class NewsCreateDeleteUpdateTest(TestCase):
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
                                       title='Some title',
                                       text='Some text',
                                       )
        cls.post.category.add(cls.category)
        # cls.user.user_permissions.set(['News.add_post', 'News.change_post', 'News.delete_post'])

    # def test_post_createview(self):
    #     # self.user.user_permissions.set('News.add_post')
    #
    #     response = self.client.post(
    #         reverse('news_create'),
    #         data={
    #             'author': self.author,
    #             'category': self.category,
    #             'title': 'New title',
    #             'text': 'New text',
    #         }, )
    #
    #     # print(f'!!!!!!!!!!!!!!!{Post.objects.all()}')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(Post.objects.last().title, "New title")
    #     self.assertEqual(Post.objects.last().text, "New text")


# def test_news_createview(self):
#     response = self.client.post(
#         reverse('news_create'),
#         {
#             'author': self.author,
#             'category': [self.category],
#             'title': 'New title',
#             'text': 'New text',
#         }
#     )
#     self.assertEqual(response.status_code, 302)
#     self.assertEqual(Post.objects.get(id=1).title, 'New title')
#     self.assertEqual(Post.objects.last().text, 'New text')

    # def test_news_editview(self):
    #     self.client.login(username='testuser', password='secret')
    #     response = self.client.post(
    #         reverse('news_update', args=[1]),
    #         {
    #             'title': 'Update title',
    #             'text': 'Update text',
    #         })
    #
    #     self.assertEqual(response.status_code, 302)
    #     self.assertEqual(Post.objects.last().title, 'Update title')
    #     self.assertEqual(Post.objects.last().text, 'Update text')

    # def test_news_deleteview(self):
    #     self.client.login(username='testuser', password='secret')
    #     response = self.client.post(reverse('news_delete'), args=[1])
    #     self.assertEqual(response.status_code, 302)


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


class ProfileTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username='testuser',
                                                        first_name='testuser_name',
                                                        last_name='testuser_last_name',
                                                        email='test@email.com',
                                                        password='secret')

        cls.author = Author.objects.create(user=cls.user)

    def test_redirect_is_not_login_for_profile(self):
        # TODO
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)
        # self.assertRedirects(response, '/accounts/login?next=/news/create/')

    def test_logged_in_uses_correct_template_for_profile(self):
        login = self.client.login(username='testuser', password='secret')
        response = self.client.get(reverse('profile'))
        self.assertEqual(str(response.context['user']), 'testuser_name testuser_last_name')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news/profile.html')

    def test_redirect_is_not_login_for_profile_edit(self):
        # TODO
        response = self.client.get(reverse('profile_edit'))
        self.assertEqual(response.status_code, 302)

    def test_logged_in_uses_correct_template_for_profile_edit(self):
        login = self.client.login(username='testuser', password='secret')
        response = self.client.get(reverse('profile_edit'))
        self.assertEqual(str(response.context['user']), 'testuser_name testuser_last_name')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news/profile_edit.html')
