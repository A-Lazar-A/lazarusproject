from django.shortcuts import render, redirect
from .models import Table
from .forms import TableForm, AuthUserForm, SignUpForm
from django.urls import reverse, reverse_lazy
from django.views.generic import DeleteView, UpdateView, CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.db.models import Sum


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


class ItemCreateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Table
    template_name = 'main/index.html'
    form_class = TableForm
    success_url = reverse_lazy('inventory')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.userID = self.request.user
        self.object.value = self.object.sellprice - self.object.price
        self.object.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        dic_sum = Table.objects.filter(userID=self.request.user).aggregate(Sum('value'))
        kwargs['sum'] = dic_sum['value__sum']
        kwargs['table'] = Table.objects.order_by('-id')
        return super().get_context_data(**kwargs)


class ItemDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'login'
    model = Table
    template_name = 'main/index.html'
    success_url = reverse_lazy('inventory')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user != self.object.userID:
            return self.handle_no_permission()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)


class ItemUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    model = Table
    template_name = 'main/index.html'
    form_class = TableForm
    success_url = reverse_lazy('inventory')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.userID = self.request.user
        self.object.value = self.object.sellprice - self.object.price
        self.object.save()
        return super().form_valid(form)


class UserLoginView(LoginView):
    model = User
    template_name = 'main/login.html'
    form_class = AuthUserForm
    success_url = reverse_lazy('inventory')

    def get_success_url(self):
        return self.success_url


class UserRegisterView(CreateView):
    model = User
    template_name = 'main/sing-up.html'
    form_class = SignUpForm
    success_url = reverse_lazy('inventory')

    def form_valid(self, form):
        form_valid = super().form_valid(form)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        auth_user = authenticate(username=username, password=password)
        login(self.request, auth_user)
        return form_valid


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('inventory')


def statistic(request):
    return render(request, 'main/statistic.html')
