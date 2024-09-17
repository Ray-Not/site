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
        'Эталон', 'Персона', 'Black', 'Bravo',
        'Бункер', 'Сенатор', 'Эврика', 'Волкодав',
        'Эврика,', 'Diva', 'Mastino', 'Ратибор',
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
        'Тип отделки: МДФ панель с фрезеровкой и пластиковым молдингом',
        'Тип отделки: ЛДСП',
        'Тип отделки: влагостойкая МДФ панель с покрытием "винорит"',
        'Тип отделки: Меламин',
        'Тип отделки: МДФ панель со стеклопакетом и ковкой',
        'Тип отделки: Металл с порошковым напылением',
        'Тип отделки: Металл, цинкосодержащий грунт, полимерное покрытие',
        'Тип отделки: МДФ панель с тонированным зеркалом',
        'Тип отделки: ДВП',
        'Тип отделки: Эмалированная МДФ панель',
        'Тип отделки: МДФ панель с покрытием "винорит"',
        'Тип отделки: гладкая МДФ панель',
        'Тип отделки: комбинированная МДФ панель',
        'Тип отделки: панель МДФ с отделкой Экошпоном и вставкой черный \
лакобель',
        'Тип отделки: Массив + Шпон',
        'Тип отделки: Меламиновая панель',
        'Тип отделки: Ламинированная МДФ',
        'Тип отделки: Gloss (Глянец)',
        'Тип отделки: МДФ панель с зеркалом',
        'Нет информации',
        'Тип отделки: Фрезерованная МДФ панель со вставкой \
черное стекло фацет',
        'Тип отделки: Ламинированная МДФ панель',
        'Тип отделки: МДФ панель с молдингами',
        'Тип отделки: МДФ панель с фрезеровкой',
        'Тип отделки: МДФ со стеклянными вставками',
        'Тип отделки: МДФ панель c атмосферостойким ламинированным покрытием',
        'Тип отделки: МДФ панель с металлическими вставками',
        'Тип отделки: МДФ панель с зеркалом фацет',
        'Тип отделки: Шпонированная панель',
        'Тип отделки: Панель Profildoors U (УФ-лак)',
        'Тип отделки: ламинированная МДФ панель',
        'Тип отделки: панель МДФ с отделкой Эко Шпоном',
        'Тип отделки: панель МДФ с отделкой Экошпоном и \
вставкой белый лакобель'
    ]
    out_covers = [
        'МДФ панель с фрезеровкой и пластиковым молдингом',
        'МДФ панель с металлическими вставками',
        'МДФ панель с зеркалом', 'гладкая МДФ панель',
        'Влагостойкая CPL панель',
        'Влаго-термостойкая панель', 'Панель из массива',
        'Металл с декоративными элементами',
        'панель МДФ с отделкой Экошпоном и вставкой черный лакобель',
        'Влагостойкая шпонированная панель Waterproof Veneer',
        'МДФ панель с фрезеровкой',
        'МДФ панель с молдингами',
        'Металл с зеркальной вставкой из нержавеющей стали',
        'Фрезерованная МДФ панель со вставкой черное стекло фацет',
        'ламинированная МДФ панель',
        'Эмалированная МДФ панель', 'Gloss (Глянец)',
        'МДФ со стеклянными вставками',
        'Металл, цинкосодержащий грунт, полимерное покрытие',
        'Металл с матовым покрытием',
        'Ламинированная МДФ', 'МДФ панель с покрытием "винорит"',
        'МДФ панель со стеклопакетом и ковкой',
        'Металл с порошковым напылением', 'Металл с выдавленным рисунком',
        'панель МДФ с отделкой Экошпоном и вставкой белый лакобель',
        'Сборная МДФ 3D-панель',
        'Ламинированная МДФ панель',
        'МДФ панель c атмосферостойким ламинированным покрытием',
        'комбинированная МДФ панель',
        'влагостойкая МДФ панель с покрытием "винорит"',
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
    selected_brands = request.GET.getlist('brand')
    selected_purposes = request.GET.getlist('purpose')
    selected_out_covers = request.GET.getlist('out_covers')
    selected_in_covers = request.GET.getlist('in_covers')

    return render(request, 'pages/catalog.html', {
        # 'doors': doors,
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
