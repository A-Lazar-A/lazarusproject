from django.shortcuts import render, redirect
from .models import Table
from .forms import TableForm


def inventory(request):
    error = ''
    if request.method == 'POST':
        form = TableForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory')
        else:
            error = 'Not valid form'

    form = TableForm()
    table = Table.objects.order_by('id')
    context = {
        'table': table,
        'form': form,
        'error': error
    }

    return render(request, 'main/index.html', context)


def login(request):
    return render(request, 'main/login.html')


def statistic(request):
    return render(request, 'main/statistic.html')
