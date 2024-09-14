from django.shortcuts import render, redirect
from .forms import OrderForm


def index(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = OrderForm()

    return render(request, 'index.html', {'form': form})


def catalog(request):
    return render(request, 'pages/catalog.html')
