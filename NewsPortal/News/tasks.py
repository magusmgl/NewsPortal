from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Category, User, Post
from datetime import datetime


@shared_task
def mailing_subscribers_after_news_creation(post_pk):
    categories = Category.objects.filter(post=post_pk)
    for cat in categories:
        # для каждой категории ищем
        category_subcribes = User.objects.filter(categorysubcribes__category=cat).values('email',
                                                                                         'first_name',
                                                                                         'last_name', )
        if category_subcribes:
            for subscribe in category_subcribes:
                html_content = render_to_string(
                    'news/adding_news_newsletter.html',
                    {
                        'instance': Post.objects.get(pk=post_pk),
                        'subscribers_name': f"{subscribe['first_name']} {subscribe['last_name']}",
                        'categories': ', '.join([f"{cat.category_name.title()}" for cat in categories])
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
def weekly_newsletter_for_subscribers():
    # Получаем список пользователей у которых есть подписка на хотя бы одна категория в подписке
    users_with_subscriptions = User.objects.filter(categorysubcribes__isnull=False).distinct()

    for user in users_with_subscriptions:
        # получаем список категорий на которые подписан конкретный пользователь
        list_of_user_categories = Category.objects.filter(subscribers__id=user.id)
        # Получаем список всех постов по категориям пользователя за 7 дней.
        list_of_post = Post.objects.filter(category__in=list_of_user_categories,
                                           date__gte=datetime.now().replace(day=datetime.now().day - 1).strftime(
                                               '%Y-%m-%d')).distinct()

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
