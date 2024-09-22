from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Max, Min
from django.shortcuts import redirect, render, get_object_or_404

from .filters import DoorFilter
from .forms import OrderForm
from .models import Door, Review, Tag, Catalog, Blog, BlogChapter, DeliveryRegion


def index(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = OrderForm()
    reviews = Review.objects.all().order_by('-id')[:6]

    return render(request, 'index.html', {
        'form': form,
        'reviews': reviews,
        'range': range(1, 6),
    })


def installation(request):

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('installation')
    else:
        form = OrderForm()
    return render(request, 'pages/installation.html', {
        'form': form,
    })


def garant(request):
    return render(request, 'pages/garant.html')


def delivery(request):

    moscow_regions = DeliveryRegion.objects.filter(region='moscow')
    moscow_region_areas = DeliveryRegion.objects.filter(region='moscow_region')

    context = {
        'moscow_regions': moscow_regions,
        'moscow_region_areas': moscow_region_areas
    }

    return render(request, 'pages/delivery.html', context)


def delivery_detail(request, slug):

    region = get_object_or_404(DeliveryRegion, slug=slug)

    context = {
        'region': region
    }

    return render(request, 'pages/delivery_detail.html', context)


def catalog(request, slug=None):
    brands = [
        'Эталон', 'Персона', 'Black', 'Bravo',
        'Бункер', 'Сенатор', 'Эврика',
        'Волкодав', 'Diva', 'Mastino',
        'Ратибор', 'Дэко', 'Леванте', 'Оптим',
        'Лекс', 'Арма', 'Баяр', 'Практик',
        'Асд', 'Морра', 'Lummix', 'Str',
        'Тефлон', 'Silver', 'Quartet',
        'Престиж', 'Противопожарные', 'Labirint',
        'Премиум', 'Ле-гран', 'Интекрон',
        'Лира', 'Rex', 'Страж', 'Profildoors',
        'Regidoors', 'Falko'
    ]
    purposes = [
        'для служебных помещений', 'уличная (необходим козырек)',
        'рекомендуется для квартиры, возможно использование в \
качестве уличной (необходим козырек и тамбур)',
        'рекомендуется в качестве уличной (необходим козырек и тамбур) \
или для квартиры',
        'противопожарная', 'только для квартиры (внутри подъезда)'
    ]
    in_covers = [
        'МДФ панель', 'ЛДСП', 'Меламин', 'Металл', 'ДВП', 'Массив + Шпон',
        'Меламиновая панель', 'Gloss (Глянец)', 'Шпонированная панель',
        'Панель Profildoors U (УФ-лак)',
    ]
    out_covers = [
        'МДФ панель', 'Влагостойкая CPL панель', 'Влаго-термостойкая панель',
        'Панель из массива', 'Металл с декоративными элементами',
        'Влагостойкая шпонированная панель Waterproof Veneer', 'Металл',
        'Влагостойкая ARTWOOD PANEL'
    ]

    # Получение выбранных тегов из запроса
    tag_titles = request.GET.getlist('tags')
    if tag_titles:
        tags_url = Tag.objects.filter(title__in=tag_titles)
    else:
        tags_url = Tag.objects.none()  # Пустой QuerySet, если нет тегов

    # В случае передачи слага
    doors_queryset = Door.objects.all().order_by('id')
    catalogs = Catalog.objects.all()
    if slug:
        catalog = get_object_or_404(Catalog, slug=slug)
        doors_queryset = doors_queryset.filter(catalogs__in=[catalog])
        print(doors_queryset)

    # Фильтрация дверей
    door_filter = DoorFilter(
        request.GET,
        queryset=doors_queryset
    )
    filtered_doors = door_filter.qs

    if tags_url:
        filtered_doors = filtered_doors.filter(tags__in=tags_url).distinct()

    # Пагинация
    paginator = Paginator(filtered_doors, 60)
    page = request.GET.get('page')
    try:
        doors = paginator.page(page)
    except PageNotAnInteger:
        doors = paginator.page(1)
    except EmptyPage:
        doors = paginator.page(paginator.num_pages)

    # Получение минимальной и максимальной цены
    min_price = Door.objects.aggregate(Min('price'))['price__min']
    max_price = Door.objects.aggregate(Max('price'))['price__max']

    # Получение выбранных фильтров
    selected_brands = (
        request.GET.get('brand', '').split(',')
        if request.GET.get('brand') else []
    )

    selected_purposes = (
        request.GET.get('purpose', '').split(',')
        if request.GET.get('purpose') else []
    )

    selected_out_covers = (
        request.GET.get('out_covers', '').split(',')
        if request.GET.get('out_covers') else []
    )

    selected_in_covers = (
        request.GET.get('in_covers', '').split(',')
        if request.GET.get('in_covers') else []
    )

    # Передача данных в шаблон
    return render(request, 'pages/catalog.html', {
        'doors': doors,
        'filter': door_filter,
        'min_price': min_price,
        'max_price': max_price,
        'brands': brands,
        'purposes': purposes,
        'out_covers': out_covers,
        'in_covers': in_covers,
        'selected_brands': selected_brands,
        'selected_purposes': selected_purposes,
        'selected_out_covers': selected_out_covers,
        'selected_in_covers': selected_in_covers,
        'tags_cloud': Tag.objects.filter(in_cloud=True),
        'catalog': catalog if slug else None,
        'catalogs': catalogs,
    })


def blog_chapter(request):
    chapters = BlogChapter.objects.all()
    chapter_blog = {}

    for chapter in chapters:
        count = chapter.blogs.count()
        chapter_blog[chapter] = count

    context = {
        'chapters': chapter_blog
    }

    return render(request, 'pages/blog_chapter.html', context)


def blog_chapter_detail(request, chapter_slug):
    chapter = get_object_or_404(BlogChapter, slug=chapter_slug)
    blogs = chapter.blogs.all()

    context = {
        'chapter': chapter,
        'blogs': blogs
    }

    return render(request, 'pages/blog_chapter_detail.html', context)


def blog_post_detail(request, chapter_slug, post_slug):
    blog = get_object_or_404(Blog, slug=post_slug)
    chapter = get_object_or_404(BlogChapter, slug=chapter_slug)

    context = {
        'chapter': chapter,
        'blog': blog
    }

    return render(request, 'pages/blog_post_detail.html', context)
