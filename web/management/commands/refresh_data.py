from django.core.management.base import BaseCommand
from web.models import Door
import random

used_numbers = set()


def generate_unique_number(min_value=1, max_value=100):
    while True:
        number = random.randint(min_value, max_value)
        if number not in used_numbers:
            used_numbers.add(number)
            return number


class Command(BaseCommand):
    help = 'Меняет название дверям'

    def handle(self, *args, **kwargs):
        doors = Door.objects.filter(title__icontains="Страж")

        count = doors.count()
        self.stdout.write(self.style.SUCCESS(f'Найдено {count} дверей'))

        # for door in doors:
        #     random_number = generate_unique_number()
        #     new_title = f"Входная металлическая дверь в квартиру Стандарт {random_number}"
        #     door.title = new_title
        #     door.save()
        #     self.stdout.write(self.style.SUCCESS(f'Обновлено: {new_title}'))
