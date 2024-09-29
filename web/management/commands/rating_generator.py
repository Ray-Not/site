from django.core.management.base import BaseCommand
from faker import Faker

from web.models import Door, Review


class Command(BaseCommand):
    help = 'Генерация положительных отзывов для дверей'

    def handle(self, *args, **kwargs):
        fake = Faker('ru_RU')  # Используем русский язык

        for i in range(0, 400):
            # Генерация положительных отзывов с рейтингом от 7 до 10
            Review.objects.create(
                name=fake.name(),
                rating=fake.random_int(min=7, max=10),
                # message=fake.text(max_nb_chars=255)
            )
            self.stdout.write(self.style.SUCCESS('Отзыв создан'))
