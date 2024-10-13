from django.core.management.base import BaseCommand
from django.db import IntegrityError

from web.models import Door
from slugify import slugify


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        doors = Door.objects.all()

        for door in doors:
            try:
                door.slug = slugify(door.title)
            except IntegrityError:
                door.slug = f"{slugify(door.title)}" + "P"
            door.description = f'Купить {door.title} 🛒 в Москве по цене {door.price} руб. 🚪 Паритет двери 🛠️'
            door.h1 = door.title
            door.save()
