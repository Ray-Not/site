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
        brands = [
            'Комфорт', 'Дионис', 'Сенатор',
            'Престиж', 'Гранд',
            'Йошкар-Ола', 'Стандарт', 'Mastino',
            'Labirint', 'Интекрон', 'Арма', 'Акрон'
        ]
        doors = Door.objects.all()

        # Итерируем по дверям и скрываем те, в title которых нет брендов
        for door in doors:
            if not any(brand in door.title for brand in brands):
                door.hidden = True
                door.save()
