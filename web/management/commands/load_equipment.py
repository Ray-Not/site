import csv

from django.core.management.base import BaseCommand

from web.models import Door


class Command(BaseCommand):
    help = 'Загружает все записи из CSV файла в базу данных'

    def handle(self, *args, **kwargs):

        csv_file = 'output_file.csv'

        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)

            for row in reader:
                title = row[0]
                equipment_data = row[1]
                print(title)
                door = Door.objects.get(slug=title)
                door.equipment = equipment_data
                door.save()
