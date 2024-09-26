import csv

from django.core.management.base import BaseCommand, CommandError

from web.models import Door


class Command(BaseCommand):
    help = 'Загружает все записи из CSV файла в базу данных'

    def handle(self, *args, **kwargs):

        csv_file = 'doors_data.csv'

    # Читаем CSV-файл
        with open(csv_file, 'r', encoding='utf-8') as file:

            cleaned_file = (line.replace('\0', '') for line in file)
            reader = csv.reader(cleaned_file)
            for row in reader:
                if not Door.objects.filter(slug=row[0]).exists():
                    print(f'Модель с {row[0]} не найдена')
