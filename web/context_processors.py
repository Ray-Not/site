from .models import Catalog
from django.db.models import Count


def catalog_context(request):
    chapters_with_titles = Catalog.objects.values(
        'chapter'
    ).annotate(titles=Count('title'))
    catalogs_btn = Catalog.objects.all().order_by('chapter', 'title')

    return {
        'chapters_with_titles': chapters_with_titles,
        'catalogs_btn': catalogs_btn,
    }
