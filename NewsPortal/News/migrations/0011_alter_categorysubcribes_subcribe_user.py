# Generated by Django 4.0.6 on 2022-08-17 18:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('News', '0010_alter_category_options_alter_post_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categorysubcribes',
            name='subcribe_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subcribe_users', to=settings.AUTH_USER_MODEL, verbose_name='Подписчик'),
        ),
    ]
