from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Max, Min
from django.shortcuts import redirect, render

from .filters import DoorFilter
from .forms import OrderForm
from .models import Door, Review


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
        'range': range(1, 11)
    })


def catalog(request):
    brands = [
        'Эталон', 'Персона', 'Black', 'Bravo',
        'Бункер', 'Сенатор', 'Эврика', 'Волкодав',
        'Diva', 'Mastino', 'Ратибор',
        'Дэко', 'Леванте', 'Оптим', 'Лекс',
        'Арма', 'Баяр', 'Практик', 'Асд', 'Морра',
        'Lummix', 'Str', 'Тефлон', 'Silver',
        'Quartet', 'Престиж', 'Противопожарные',
        'Labirint', 'Премиум', 'Ле-гран',
        'Интекрон', 'Лира', 'Rex', 'Страж', 'Profildoors', 'Regidoors', 'Falko'
    ]
    purposes = [
        'для служебных помещений', 'уличная (необходим козырек)',
        'рекомендуется для квартиры, возможно использование в качестве \
уличной (необходим козырек и тамбур)', 'рекомендуется в качестве уличной \
(необходим козырек и тамбур) или для квартиры',
        'противопожарная', 'только для квартиры (внутри подъезда)'
    ]
    in_covers = [
        'МДФ панель',
        'ЛДСП',
        'Меламин',
        'Металл',
        'ДВП',
        'Массив + Шпон',
        'Меламиновая панель',
        'Gloss (Глянец)',
        'Шпонированная панель',
        'Панель Profildoors U (УФ-лак)',
    ]
    out_covers = [
        'МДФ панель',
        'Влагостойкая CPL панель',
        'Влаго-термостойкая панель', 'Панель из массива',
        'Металл с декоративными элементами',
        'Влагостойкая шпонированная панель Waterproof Veneer',
        'Металл',
        'Влагостойкая ARTWOOD PANEL'
    ]
    door_filter = DoorFilter(
        request.GET,
        queryset=Door.objects.all().order_by('id')
    )
    filtered_doors = door_filter.qs
    min_price = Door.objects.aggregate(Min('price'))['price__min']
    max_price = Door.objects.aggregate(Max('price'))['price__max']
    paginator = Paginator(filtered_doors, 20)
    page = request.GET.get('page')

    try:
        doors = paginator.page(page)
    except PageNotAnInteger:
        doors = paginator.page(1)
    except EmptyPage:
        doors = paginator.page(paginator.num_pages)

    # Get selected brands from request.GET
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
    })
