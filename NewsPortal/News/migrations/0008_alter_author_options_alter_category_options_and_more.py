# Generated by Django 4.0.6 on 2022-08-16 05:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('News', '0007_categorysubcribes_category_subscribers_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'verbose_name': 'Автор', 'verbose_name_plural': 'Авторы'},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'verbose_name': 'Пост', 'verbose_name_plural': 'Посты'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
        migrations.RemoveField(
            model_name='categorysubcribes',
            name='user',
        ),
        migrations.AddField(
            model_name='categorysubcribes',
            name='subcribe_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Подписчик'),
        ),
        migrations.AlterField(
            model_name='author',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='author', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='author',
            name='user_rating',
            field=models.SmallIntegerField(db_column='rating', default=0, verbose_name='Рейтинг пользователя'),
        ),
        migrations.AlterField(
            model_name='category',
            name='category_name',
            field=models.CharField(db_column='name', max_length=64, unique=True, verbose_name='Имя категории'),
        ),
        migrations.AlterField(
            model_name='categorysubcribes',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='News.category', verbose_name='Категория'),
        ),
    ]