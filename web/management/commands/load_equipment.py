import csv

from django.core.management.base import BaseCommand

from web.models import Door


class Command(BaseCommand):
    help = 'Загружает все записи из CSV файла в базу данных'

    def handle(self, *args, **kwargs):

        csv_file = 'doors_data.csv'

        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)

            for row in reader:
                title = row[0]
                equipment_data = row[1]
                print(title)
                if Door.objects.filter(slug=title).exists():
                    door = Door.objects.get(slug=title)
                    door.equipment = equipment_data
                    door.save()
                else:
                    print('NF')
