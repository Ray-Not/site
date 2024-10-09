from random import sample
from django.db.models import Count
from .models import Catalog, Door
from .forms import OrderForm, CallBackForm
from django.contrib import messages
from django.shortcuts import redirect

def footer_context(request):
    # Querying catalogs with door counts
    catalogs_with_door_count = Catalog.objects.annotate(
        door_count=Count('catalogs')
    ).order_by('chapter', 'title')

    # Random catalogs with images
    catalogs_with_images = Catalog.objects.exclude(
        image=''
    ).exclude(image__isnull=True)
    if catalogs_with_images.count() <= 15:
        random_catalogs = list(catalogs_with_images)
    else:
        random_catalog_ids = sample(
            catalogs_with_images.values_list('id', flat=True), 15
        )
        random_catalogs = Catalog.objects.filter(id__in=random_catalog_ids)

    # Random catalogs for footer
    catalogs_in_footer = Catalog.objects.all()
    if catalogs_in_footer.count() <= 8:
        random_catalogs_in_footer = list(catalogs_in_footer)
    else:
        random_catalog_ids = sample(list(catalogs_in_footer.values_list(
            'id',
            flat=True
        )), 8)
        random_catalogs_in_footer = Catalog.objects.filter(
            id__in=random_catalog_ids
        )

    # Organizing catalogs by chapters
    chapters_with_titles = {}
    for catalog in catalogs_with_door_count:
        chapter = catalog.chapter
        if not chapter:
            print(f"Ошибка: пустое значение для chapter в {catalog}")
            continue  # Skip catalogs with empty chapter

        if chapter not in chapters_with_titles:
            chapters_with_titles[chapter] = []
        chapters_with_titles[chapter].append(catalog)

    # Random doors
    total_count = Door.objects.count()
    if total_count <= 8:
        random_doors = list(Door.objects.all())
    else:
        random_ids = sample(list(Door.objects.values_list('id', flat=True)), 8)
        random_doors = Door.objects.filter(id__in=random_ids)

    # Handling the callback form
    form_callback = CallBackForm(request.POST or None)

    if request.method == 'POST':
        if form_callback.is_valid():
            form_callback.save()
            form_callback = CallBackForm()

    context = {
        'form_footer': OrderForm(),
        'form_callback': form_callback,
        'chapters_with_titles': chapters_with_titles,
        'random_doors': random_doors,
        'random_catalogs': random_catalogs,
        'random_catalogs_in_footer': random_catalogs_in_footer
    }

    print("Контекст перед рендерингом:", context)
    return context
