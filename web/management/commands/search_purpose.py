from django.core.management.base import BaseCommand
from ...models import Door

purpose = set()


class Command(BaseCommand):
    help = 'Ищет бренды из БД'

    def handle(self, *args, **kwargs):
        all_doors = Door.objects.all()
        for door in all_doors:
            purpose.add(door.purpose)
        print(purpose)
