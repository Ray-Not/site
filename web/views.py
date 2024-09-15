from django.shortcuts import render, redirect
from .forms import OrderForm
from .models import Review, Door


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
    doors = Door.objects.all()
    print(doors)
    return render(request, 'pages/catalog.html', {
        'doors': doors,
    })
