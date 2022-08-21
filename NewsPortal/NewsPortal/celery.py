import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPortal.settings')

app = Celery('NewsPortal')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


app.conf.beat_schedule = {
    'action_every_monday': {
        'task': 'News.tasks.weekly_newsletter_for_subscribers',
        'schedule': crontab(day_of_week='monday', hour='12', minute='0'),
        'args': (),
    },
}
