from django.shortcuts import render, redirect
from .models import Table
from .forms import TableForm
from django.urls import reverse
from django.views.generic import DeleteView, UpdateView


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

    table = Table.objects.order_by('-id')
    context = {
        'table': table,
        'form': form,
        'error': error
    }

    return render(request, 'main/index.html', context)


def item_delete(request, pk):
    get_item = Table.objects.get(pk=pk)
    get_item.delete()
    return redirect(reverse('inventory'))


class ItemUpdateView(UpdateView):
    model = Table
    template_name = 'main/index.html'
    fields = ["title", "size", "price", "sellprice", "anyprice", "datebuy", "datesell", "notes"]
    form_class = TableForm()


# def item_edit(request, pk):
#     get_item = Table.objects.get(pk=pk)
#     context ={
#         'get_item': get_item,
#         'form': TableForm(instance=get_item)
#     }
#     return render(request, 'main/index.html', context)


def login(request):
    return render(request, 'main/login.html')


def statistic(request):
    return render(request, 'main/statistic.html')



