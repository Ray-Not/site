from django.core.management.base import BaseCommand

from ...models import Door

in_cover = set()


class Command(BaseCommand):
    help = 'Внутренняя отделка в БД'

    def handle(self, *args, **kwargs):
        all_doors = Door.objects.all()
        for door in all_doors:
            in_cover.add(door.in_cover_name)
        print(in_cover)
