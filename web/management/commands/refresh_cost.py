from django.core.management.base import BaseCommand

from web.models import DeliveryRegion


class Command(BaseCommand):
    help = 'Загружает все записи из CSV файла в базу данных'

    def handle(self, *args, **kwargs):

        regions = DeliveryRegion.objects.all()

        for region in regions:
            region.cost = 1500
            region.save()
