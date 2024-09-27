from django.db.models import Count

from .models import Catalog, Door
from random import sample


def catalog_context(request):
    catalogs_with_door_count = Catalog.objects.annotate(
        door_count=Count('catalogs')
    ).order_by('chapter', 'title')

    chapters_with_titles = {}
    for catalog in catalogs_with_door_count:
        chapter = catalog.chapter
        if chapter not in chapters_with_titles:
            chapters_with_titles[chapter] = []
        chapters_with_titles[chapter].append(catalog)

    random_doors = list(Door.objects.all())
    random_doors = sample(random_doors, min(4, len(random_doors)))

    return {
        'chapters_with_titles': chapters_with_titles,
        'random_doors': random_doors,
    }
