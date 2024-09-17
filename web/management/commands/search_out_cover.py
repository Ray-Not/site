from django.core.management.base import BaseCommand

from ...models import Door

out_cover = set()


class Command(BaseCommand):
    help = 'Внешняя отделка в БД'

    def handle(self, *args, **kwargs):
        all_doors = Door.objects.all()
        for door in all_doors:
            out_cover.add(door.out_cover_name)
        print(out_cover)
