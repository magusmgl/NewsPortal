import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util
from datetime import datetime
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


logger = logging.getLogger(__name__)

from News.models import User, Category, Post

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


# The `close_old_connections` decorator ensures that database connections, that have become
# unusable or are obsolete, are closed before and after your job has run. You should use it
# to wrap any jobs that you schedule that access the Django database in any way.
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age` from the database.
    It helps to prevent the database from filling up with old historical records that are no
    longer useful.

    :param max_age: The maximum length of time to retain historical job execution records.
                    Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            weekly_newsletter_for_subscribers,
            trigger=CronTrigger(
                day_of_week='monday', hour='08', minute='00'
            ),
            id="weekly_newsletter",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'weekly_newsletter'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
