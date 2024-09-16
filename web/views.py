from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import redirect, render
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
    doors_list = Door.objects.all().order_by('id')
    paginator = Paginator(doors_list, 20)

    page = request.GET.get('page')
    try:
        doors = paginator.page(page)
    except PageNotAnInteger:
        doors = paginator.page(1)
    except EmptyPage:
        doors = paginator.page(paginator.num_pages)

    return render(request, 'pages/catalog.html', {
        'doors': doors,
    })
