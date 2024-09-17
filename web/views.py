from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import redirect, render
from .forms import OrderForm
from .models import Door, Review
from .filters import DoorFilter
from django.db.models import Min, Max


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
        'Эталон', 'Персона', 'Black', 'Bravo', 'Бункер', 'Сенатор', 'Эврика', 'Волкодав',
        'Эврика,', 'Diva', 'Mastino', 'Ратибор', 'Дэко', 'Леванте', 'Оптим', 'Лекс',
        'Арма', 'Баяр', 'Практик', 'Асд', 'Морра', 'Lummix', 'Str', 'Тефлон', 'Silver',
        'Quartet', 'Престиж', 'Противопожарные', 'Labirint', 'Премиум', 'Ле-гран',
        'Интекрон', 'Лира', 'Rex', 'Страж', 'Profildoors', 'Regidoors', 'Falko'
    ]
    purposes = [
        'для служебных помещений', 'уличная (необходим козырек)', 'рекомендуется для квартиры, возможно использование в качестве уличной (необходим козырек и тамбур)',
        'рекомендуется в качестве уличной (необходим козырек и тамбур) или для квартиры', 'противопожарная', 'только для квартиры (внутри подъезда)'
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
    selected_brands = request.GET.getlist('brand')
    selected_purposes = request.GET.getlist('purpose')
    return render(request, 'pages/catalog.html', {
        'doors': doors,
        'filter': door_filter,
        'min_price': min_price,
        'max_price': max_price,
        'brands': brands,
        'purposes': purposes,
        'selected_brands': selected_brands,
        'selected_purposes': selected_purposes
    })
