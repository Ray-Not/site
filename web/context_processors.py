from django.db.models import Count
from .models import Catalog


def catalog_context(request):
    # Получаем каталоги и подсчитываем количество дверей для каждого каталога
    catalogs_with_door_count = Catalog.objects.annotate(
        door_count=Count('catalogs')  # Подсчет количества дверей
    ).order_by('chapter', 'title')

    # Группируем каталоги по главам
    chapters_with_titles = {}
    for catalog in catalogs_with_door_count:
        chapter = catalog.chapter
        if chapter not in chapters_with_titles:
            chapters_with_titles[chapter] = []
        chapters_with_titles[chapter].append(catalog)

    return {
        'chapters_with_titles': chapters_with_titles,
    }
