from django.core.management.base import BaseCommand

from web.models import Catalog


class Command(BaseCommand):
    help = 'Загружает все записи из CSV файла в базу данных'

    def handle(self, *args, **kwargs):

        regions = Catalog.objects.filter(image=1)

        for region in regions:
            region.image = None
            region.save()
