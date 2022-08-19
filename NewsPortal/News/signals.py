from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import Post, Category, User, PostCategory


@receiver(m2m_changed, sender=PostCategory)
def notify_subcribes_to_add_news(sender, instance, action, **kwargs):
    if action == 'post_add':
        # ищем все категории, которым принадлежит пост
        categories = Category.objects.filter(post=instance)
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
                            'instance': instance,
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
