from django.core.management.base import BaseCommand

from web.models import Door


class Command(BaseCommand):
    help = 'Загружает все записи из CSV файла в базу данных'

    def handle(self, *args, **kwargs):

        doors = Door.objects.all()

        for door in doors:
            door.price = door.price * 1.1
            door.save()
