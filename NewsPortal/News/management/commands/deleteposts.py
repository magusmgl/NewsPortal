from django.core.management.base import BaseCommand, CommandError
from News.models import Post, Category


class Command(BaseCommand):
    help = 'Удаляет все новости из указанной категории'
    missing_args_message = 'Укажите название категории, из которой нужно удалить новости'
    requires_migrations_checks = True

    def add_arguments(self, parser):
        parser.add_argument('category', nargs='+', type=str)

    def handle(self, *args, **options):
        self.stdout.readable()
        self.stdout.write(f'Вы действителньо хотите удалить все новости из категории "{options["category"]}"?(да/нет): ',
                          ending='')
        answer = input()

        if answer != 'да':
            self.stdout.write(self.style.ERROR('Отменено'))
            return

        try:
            category = Category.get(category_name=options['category'])
            Post.objects.filter(category=category).delete()
            self.stdout.write(self.style.SUCCESS('Новости удалены!'))

        except Category.DoesNotExist:
            raise CommandError(f'Категории {options["category"]} не существует!')


