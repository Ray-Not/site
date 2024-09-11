import csv
import re

from django.core.management.base import BaseCommand, CommandError

brands = set()


class Command(BaseCommand):
    help = 'Загружает все записи из CSV файла в базу данных'

    def handle(self, *args, **kwargs):
        csv_file = 'doors_data.csv'

        try:
            with open(csv_file, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                count = 0

                for row in reader:
                    count += 1
                    match = re.search(
                        r'(?:дверь|стальная дверь)?\s*(\S+)',
                        row['title'],
                        re.IGNORECASE
                    )
                    if match:
                        brands.add(match.group(1).capitalize())
                    else:
                        self.stdout.write(
                            self.style.ERROR('Заголовок не был найден')
                        )
            print(brands)
        except FileNotFoundError:
            raise CommandError(f'Файл {csv_file} не найден')

        except Exception as e:
            raise CommandError(f'Ошибка при поиске данных: {e}')
