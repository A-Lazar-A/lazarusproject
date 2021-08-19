from django.shortcuts import render, redirect
from .models import Table
from .forms import TableForm
from django.urls import reverse, reverse_lazy
from django.views.generic import DeleteView, UpdateView, CreateView


# def inventory(request):
#     error = ''
#     if request.method == 'POST':
#         form = TableForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('inventory')
#         else:
#             error = 'Not valid form'
#     form = TableForm()
#
#     table = Table.objects.order_by('-id')
#     context = {
#         'table': table,
#         'form': form,
#         'error': error
#     }
#
#     return render(request, 'main/index.html', context)


class ItemCreateView(CreateView):
    model = Table
    template_name = 'main/index.html'
    form_class = TableForm
    success_url = reverse_lazy('inventory')

    def get_context_data(self, **kwargs):
        kwargs['table'] = Table.objects.order_by('-id')
        return super().get_context_data(**kwargs)


class ItemDeleteView(DeleteView):
    model = Table
    template_name = 'main/index.html'
    success_url = reverse_lazy('inventory')


class ItemUpdateView(UpdateView):
    model = Table
    template_name = 'main/index.html'
    form_class = TableForm
    success_url = reverse_lazy('inventory')


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
