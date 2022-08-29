from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Category, User, Post
from datetime import datetime


def get_category_subcribers(category):
    '''Ищет всех подписчиков переданной категории и возвращает их почту, имя и фамилию'''
    category_subcribes = User.objects.filter(categorysubcribes__category=category).values('email',
                                                                                          'first_name',
                                                                                          'last_name', )
    return category_subcribes


def send_newsletter_when_adding_post(post_pk, subscribe, categories):
    '''Заполняет html письма и отправляет его подписчику'''
    html_content = render_to_string(
        'news/adding_news_newsletter.html',
        {
            'instance': Post.objects.get(pk=post_pk),
            'subscribers_name': f"{subscribe['first_name']} {subscribe['last_name']}",
            'categories': ', '.join([f"{category.category_name.title()}" for category in categories])
        }
    )

    msg = EmailMultiAlternatives(
        subject=f'Новая статья на сайте Cb.ru',
        from_email='magus.mgl@mail.ru',
        to=[subscribe['email']],
    )
    msg.attach_alternative(html_content, "text/html")  # добавляем html
    msg.send()  # отсылаем


@shared_task
def mailing_subscribers_after_news_creation(post_pk):
    '''Отправляет письмо подписчикам категории после добавление новости'''
    categories = Category.objects.filter(post=post_pk)
    for category in categories:
        category_subcribes = get_category_subcribers(category)
        if category_subcribes:
            for subscribe in category_subcribes:
                send_newsletter_when_adding_post(post_pk, subscribe, categories)


def get_list_of_user_categories(user):
    '''Получает список категорий на которые подписан пользователь'''
    return Category.objects.filter(subscribers__id=user.id)


def get_weekly_post_in_categories(categories):
    '''Получает список всех новостей категорий за неделю'''
    return Post.objects.filter(category__in=categories,
                               date__gte=datetime.now().replace(day=datetime.now().day - 7).strftime(
                                   '%Y-%m-%d')).distinct()


def send_weekly_newsletter_subscribers(user, list_of_post):
    '''Заполяет шаблони письма и отправляет его пользователю'''
    html_content = render_to_string(
        'news/weekly_newsletter_to_subscribers.html',
        {
            'user': user,
            'list_of_post': list_of_post,
        }
    )

    msg = EmailMultiAlternatives(
        subject=f'Еженедельная рассылка новостей от портала Cb.ru',
        from_email='magus.mgl@mail.ru',
        to=[user.email],
    )
    msg.attach_alternative(html_content, "text/html")  # добавляем html
    msg.send()  # отсылаем


@shared_task
def weekly_newsletter_for_subscribers():
    # Получаем список пользователей у которых есть подписка на хотя бы одна категория в подписке
    users_with_subscriptions = User.objects.filter(categorysubcribes__isnull=False).distinct()

    for user in users_with_subscriptions:
        # получаем список категорий на которые подписан конкретный пользователь
        list_of_user_categories = get_list_of_user_categories(user)
        # Получаем список всех постов по категориям пользователя за 7 дней.
        list_of_post = get_weekly_post_in_categories(list_of_user_categories)
        send_weekly_newsletter_subscribers(user, list_of_post)
