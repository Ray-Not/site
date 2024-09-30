from random import sample

from django.db.models import Count

from .models import Catalog, Door


def footer_context(request):
    catalogs_with_door_count = Catalog.objects.annotate(
        door_count=Count('catalogs')
    ).order_by('chapter', 'title')

    catalogs = Catalog.objects.all()


    print(catalogs)

    chapters_with_titles = {}
    for catalog in catalogs_with_door_count:
        chapter = catalog.chapter
        if chapter not in chapters_with_titles:
            chapters_with_titles[chapter] = []
        chapters_with_titles[chapter].append(catalog)

    total_count = Door.objects.count()
    if total_count <= 4:
        random_doors = list(Door.objects.all())
    else:
        random_ids = sample(list(Door.objects.values_list('id', flat=True)), 4)
        random_doors = Door.objects.filter(id__in=random_ids)

    return {
        'chapters_with_titles': chapters_with_titles,
        'random_doors': random_doors,
    }
