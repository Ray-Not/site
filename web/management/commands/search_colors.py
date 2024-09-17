import csv
import re

from django.core.management.base import BaseCommand, CommandError

brands = set()


class Command(BaseCommand):
    help = 'Ищет цвета в файле'

    def handle(self, *args, **kwargs):
        csv_file = 'doors_data.csv'

        try:
            with open(csv_file, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                count = 0

                for row in reader:
                    count += 1
                    title = row['title']
                    print(f"Обрабатываемая строка: {title}")

                    # Поиск цвета в title
                    match = re.search(
                        r'(?:Цвет\s*)?["“”]{1,2}([^"“”]+)["“”]{1,2}',
                        title,
                        re.IGNORECASE
                    )
                    if match:
                        # Используем либо первую, либо вторую группу
                        color = match.group(1) or match.group(2)
                        brands.add(color.capitalize())
                    else:
                        self.stdout.write(
                            self.style.ERROR(
                                f'Цвет не найден в строке: {title}'
                            )
                        )

            print(brands)
        except FileNotFoundError:
            raise CommandError(f'Файл {csv_file} не найден')

        except Exception as e:
            raise CommandError(f'Ошибка при поиске данных: {e}')
