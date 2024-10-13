from django.core.management.base import BaseCommand
from django.db import IntegrityError
from web.models import Door
from slugify import slugify


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        doors = Door.objects.only('id', 'title', 'price', 'slug', 'description', 'h1')

        updated_doors = []
        for door in doors:
            new_slug = slugify(door.title)
            if Door.objects.filter(slug=new_slug).exists():
                new_slug += 'P'

            new_description = f'Купить {door.title} 🛒 в Москве по цене {door.price} руб. 🚪 Паритет двери 🛠️'

            # Проверяем, нужно ли обновлять объект
            if (door.slug != new_slug or 
                door.description != new_description or 
                door.h1 != door.title):
                
                door.slug = new_slug
                door.description = new_description
                door.h1 = door.title
                updated_doors.append(door)

        # Пакетное обновление измененных объектов
        if updated_doors:
            Door.objects.bulk_update(updated_doors, ['slug', 'description', 'h1'])
