import locale
from datetime import datetime, timedelta
import json
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Avg, Max, Min
from django.shortcuts import get_object_or_404, redirect, render

from .filters import DoorFilter
from .forms import CustomOrderForm, OrderForm, ReviewForm, GetDiscountForm
from .models import (Blog, BlogChapter, Catalog, DeliveryRegion, Door, Order,
                     Review, Tag)
from django.views.decorators.csrf import csrf_exempt


def index(request):
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

    min_price = Door.objects.aggregate(Min('price'))['price__min']
    max_price = Door.objects.aggregate(Max('price'))['price__max']

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
        'min_price': min_price,
        'max_price': max_price,
        'brands': brands,
        'purposes': purposes,
        'out_covers': out_covers,
        'in_covers': in_covers,
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
        'region': region,
        'tags_cloud': Catalog.objects.order_by('?')[:4],
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

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = OrderForm()

    # В случае передачи слага
    doors_queryset = Door.objects.all().order_by('id')
    catalogs = Catalog.objects.all()
    if slug:
        catalog = get_object_or_404(Catalog, slug=slug)
        doors_queryset = doors_queryset.filter(catalogs__in=[catalog])

    search = request.GET.get('search')

    if search:
        doors_queryset = doors_queryset.filter(title__icontains=search)

    # Фильтрация дверей
    door_filter = DoorFilter(
        request.GET,
        queryset=doors_queryset
    )
    filtered_doors = door_filter.qs

    if tags_url:
        filtered_doors = filtered_doors.filter(tags__in=tags_url).distinct()

    # Пагинация
    paginator = Paginator(filtered_doors, 30)
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

    page_number = request.GET.get('page', 1)

    # Передача данных в шаблон
    return render(request, 'pages/catalog.html', {
        'form': form,
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
        'tags_cloud': Catalog.objects.order_by('?')[:4],
        'catalog': catalog if slug else None,
        'catalogs': catalogs,
        'page': page_number
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


def door_detail(request, slug):

    door = get_object_or_404(Door, slug=slug)
    images = door.images.split(',')
    equipment_data = door.equipment.split(';')
    equipment_list = []
    min_price = Door.objects.aggregate(Min('price'))['price__min']
    max_price = Door.objects.aggregate(Max('price'))['price__max']
    average_rating = Review.objects.aggregate(Avg('rating'))['rating__avg']

    if average_rating is not None:
        average_rating = round(average_rating / 2, 1)
        average_rating = str(average_rating).replace(',', '.')
    else:
        average_rating = '9.0'

    door_count = Door.objects.count()

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.door = door
            order.save()
            return redirect('door_detail', slug=door.slug)
    else:
        form = OrderForm()

    if request.method == 'POST':
        discount_form = GetDiscountForm(request.POST)
        if discount_form.is_valid():
            order = discount_form.save(commit=False)
            order.door = door
            order.save()
            return redirect('door_detail', slug=door.slug)
    else:
        discount_form = GetDiscountForm()

    for item in equipment_data:
        parts = item.split(',')
        if len(parts) == 2:
            equipment_list.append({
                'name': parts[0].strip(),
                'image_url': parts[1].strip()
            })

    characteristics = {
        'purpose': door.purpose,
        'conturs_name': door.conturs_name,
        'size_name': door.size_name,
        'steel_size': door.steel_size,
        'tolshina': door.tolshina,
        'korob_size': door.korob_size,
        'uteplitel': door.uteplitel,
        'ves': door.ves,
        'constr_korob': door.constr_korob,
        'constr_fixator': door.constr_fixator,
        'zamok1': door.zamok1,
        'zamok2': door.zamok2,
        'furn_color_name': door.furn_color_name,
        'petli': door.petli,
        'zadvijka': door.zadvijka,
        'ruchka': door.ruchka,
        'glazok': door.glazok,
        'cilindr': door.cilindr,
        'bronia': door.bronia,
    }

    out_characteristics = {
        'out_cover_name': door.out_cover_name,
        'out_color': door.out_color,
    }

    in_characteristics = {
        'in_thick': door.in_thick,
        'in_color': door.in_color,
    }

    images = door.images.split(',')

    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
    delivery_date = datetime.now() + timedelta(days=3)
    catalog_tags = door.catalogs_cloud.all()  # Или другой способ получения тегов для двери

    # Если catalog_tags пустой, берем 4 случайных тега
    if not catalog_tags.exists():
        tags_cloud = Catalog.objects.order_by('?')[:4]
    else:
        tags_cloud = catalog_tags

    context = {
        'door': door,
        'characteristics': characteristics,
        'images': images,
        'out_characteristics': out_characteristics,
        'in_characteristics': in_characteristics,
        'equipment_list': equipment_list,
        'form': form,
        'discount_form': discount_form,
        'min_price': min_price,
        'max_price': max_price,
        'avg_rating': average_rating,
        'door_count': door_count,
        'delivery_date': delivery_date.strftime('%d %B'),
        'tags_cloud': tags_cloud,
    }
    return render(request, 'pages/door_detail.html', context)


def reviews(request):
    reviews = Review.objects.all()
    paginator = Paginator(reviews, 20)
    page_number = request.GET.get('page')

    try:
        reviews = paginator.page(page_number)
    except PageNotAnInteger:
        reviews = paginator.page(1)
    except EmptyPage:
        reviews = paginator.page(paginator.num_pages)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            order_number = form.cleaned_data['order_number']

            try:
                order = Order.objects.get(order_number=order_number)

                if hasattr(order, 'review'):
                    form.add_error(
                        'order_number',
                        'Отзыв для данного заказа уже существует.'
                    )
                else:
                    review = form.save(commit=False)
                    review.order = order
                    review.door = order.door
                    review.save()
                    return redirect('reviews')

                return redirect('reviews')
            except Order.DoesNotExist:
                form.add_error(
                    'order_number',
                    'Заказ с таким номером не существует.'
                )
            return redirect('reviews')
    else:
        form = ReviewForm()

    context = {
        'range_10': range(10),
        'form': form,
        'reviews': reviews,
        'range': range(1, 6),
        'page': page_number
    }

    return render(request, 'pages/reviews.html', context)


def contact(request):
    return render(request, 'pages/contact.html')


def shop_card(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Сохраняем общую информацию о заказе
            common_order_info = form.cleaned_data

            # Получаем данные из корзины
            cart_data = json.loads(request.POST.get('cart_data', '[]'))

            # Обрабатываем каждую дверь в корзине
            for item in cart_data:
                title = item.get('title')  # Получаем заголовок
                # Находим дверь по заголовку
                door = get_object_or_404(Door, title=title)

                # Создаем новый заказ для каждой двери
                order = Order(
                    name=common_order_info['name'],
                    phone=common_order_info['phone'],
                    call_time=common_order_info['call_time'],
                    address=common_order_info['address'],
                    message=common_order_info['message'],
                    door=door  # Привязываем дверь к заказу
                )
                order.save()  # Сохраняем новый заказ

            return redirect('shop_card')
    else:
        form = OrderForm()

    context = {
        'form': form,
    }
    return render(request, 'pages/shop_card.html', context)


def custom_404_view(request, exception):
    return render(request, '404.html', status=404)


@csrf_exempt
def compare_doors(request):
    if request.method == 'GET':
        door_ids = request.GET.get('door_ids', '')
        door_ids = [int(id) for id in door_ids.split(',') if id.isdigit()]
        request.session['compareList'] = door_ids

    door_ids = request.session.get('compareList', [])
    doors_to_compare = Door.objects.filter(id__in=door_ids)

    return render(request, 'pages/compare.html', {
        'doors': doors_to_compare
    })


def calculator(request):
    if request.method == 'POST':
        form = CustomOrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/calc/')
    else:
        form = CustomOrderForm()

    context = {
        'form': form
    }

    return render(request, 'pages/calculator.html', context)
