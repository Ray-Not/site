import csv

from django.core.management.base import BaseCommand

from web.models import Door, Equipment


class Command(BaseCommand):
    help = 'Загружает все записи из CSV файла в базу данных'

    def handle(self, *args, **kwargs):

        csv_file = 'output_file.csv'

        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)

            for row in reader:
                title = row[0]
                # equipment_data = row[1]
                print(row[0])
                door, _ = Door.objects.get_or_create(slug=title)
                # equipment_items = equipment_data.split(';')
                # for item in equipment_items:
                #     name, image_path = item.split(', ', 1)
                #     print(name, image_path)
                    # door.equipment.add(equipment)

                door.save()
