from django.core.management.base import BaseCommand
from web.models import Door, Catalog
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
        # Список брендов и соответствующих каталогов
        brands_catalog_mapping = {
            'Комфорт': 'Комфорт (производитель)',
            'Дионис': 'Дионис',
            'Сенатор': 'Сенатор',
            'Престиж': 'Престиж',
            'Гранд': 'Гранд',
            'Йошкар-Ола': 'Йошкар-Ола',
            'Стандарт': 'Стандарт',
            'Mastino': 'Mastino',
            'Labirint': 'Labirint',
            'Интекрон': 'Интекрон',
            'Арма': 'Арма',
            'Акрон': 'Акрон'
        }

        # Получаем все скрытые двери
        hidden_doors = Door.objects.filter(hidden=False)

        # Проходим по всем дверям, добавляем в каталоги
        for door in hidden_doors:
            for brand, catalog_title in brands_catalog_mapping.items():
                if brand in door.title:
                    # Ищем каталог по его title
                    catalog = Catalog.objects.get(title=catalog_title)
                    
                    # Проверяем, находится ли дверь уже в этом каталоге
                    if catalog not in door.catalogs.all():
                        # Добавляем каталог к ManyToMany-полю catalogs у двери
                        door.catalogs.add(catalog)
                        # Сохраняем изменения
                        door.save()
                        print(f'Дверь "{door.title}" добавлена в каталог "{catalog_title}".')
                    else:
                        print(f'Дверь "{door.title}" уже находится в каталоге "{catalog_title}".')
