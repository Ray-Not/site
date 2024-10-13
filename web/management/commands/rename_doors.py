from django.core.management.base import BaseCommand
from web.models import Door
from slugify import slugify


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        doors = Door.objects.all()

        for door in doors:
            base_slug = slugify(door.title)
            unique_slug = self.get_unique_slug(base_slug)

            door.slug = unique_slug
            door.description = f'Купить {door.title} 🛒 в Москве по цене {door.price} руб. 🚪 Паритет двери 🛠️'
            door.h1 = door.title
            door.save()

    def get_unique_slug(self, base_slug):
        """
        Функция для генерации уникального slug.
        Если slug уже существует, добавляется суффикс с номером.
        """
        slug = base_slug
        counter = 1
        # Проверка на существование такого slug
        while Door.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug
