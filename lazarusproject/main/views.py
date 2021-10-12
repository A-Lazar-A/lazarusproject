from datetime import timedelta

from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import DeleteView, UpdateView, CreateView, TemplateView, FormView, ListView

from .forms import TableForm, AuthUserForm, SignUpForm, MeetingForm
from .models import Table, Meetings


class MainTemplateView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    template_name = 'main/index.html'
    model = Table

    def get_context_data(self, *, object_list=None, **kwargs):
        last_year = timezone.now().date() - timedelta(days=365)
        last_month = timezone.now().date() - timedelta(days=30)
        some_day_last_week = timezone.now().date() - timedelta(days=7)
        year_sum = Table.objects.filter(datesell__gte=last_year, userID=self.request.user).aggregate(Sum('sellprice'))
        year_sum['sellprice__sum'] = None or year_sum['sellprice__sum'] or 0
        week_sum = Table.objects.filter(datesell__gte=some_day_last_week, userID=self.request.user).aggregate(
            Sum('sellprice'))
        week_sum['sellprice__sum'] = None or week_sum['sellprice__sum'] or 0
        month_sum = Table.objects.filter(datesell__gte=last_month, userID=self.request.user).aggregate(Sum('sellprice'))
        month_sum['sellprice__sum'] = None or month_sum['sellprice__sum'] or 0
        year_sum_b = Table.objects.filter(datebuy__gte=last_year, userID=self.request.user).aggregate(Sum('price'))
        year_sum_b['price__sum'] = None or year_sum_b['price__sum'] or 0
        week_sum_b = Table.objects.filter(datebuy__gte=some_day_last_week, userID=self.request.user).aggregate(
            Sum('price'))
        week_sum_b['price__sum'] = None or week_sum_b['price__sum'] or 0
        month_sum_b = Table.objects.filter(datebuy__gte=last_month, userID=self.request.user).aggregate(Sum('price'))
        month_sum_b['price__sum'] = None or month_sum_b['price__sum'] or 0
        year_value = year_sum['sellprice__sum'] - year_sum_b['price__sum']
        month_value = month_sum['sellprice__sum'] - month_sum_b['price__sum']
        week_value = week_sum['sellprice__sum'] - week_sum_b['price__sum']
        dic_sum = Table.objects.filter(userID=self.request.user).aggregate(Sum('value'))
        dic_sum['value__sum'] = None or dic_sum['value__sum'] or 0
        item_form = TableForm(self.request.GET or None)
        meetings_form = MeetingForm(self.request.GET or None)
        kwargs['form'] = item_form
        kwargs['meetings_form'] = meetings_form
        kwargs['year_value'] = year_value
        kwargs['month_value'] = month_value
        kwargs['week_value'] = week_value
        kwargs['sum'] = dic_sum['value__sum']
        kwargs['table'] = Table.objects.order_by('-id')
        return super().get_context_data(**kwargs)

    # def get(self, request, *args, **kwargs):
    #     item_form = TableForm(self.request.GET or None)
    #     meetings_form = MeetingForm(self.request.GET or None)
    #     context = self.get_context_data(**kwargs)
    #     context['form'] = item_form
    #     context['meetings_form'] = meetings_form
    #     return self.render_to_response(context)


class MeetingsListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    template_name = 'main/meetings.html'
    model = Meetings

    def get_context_data(self, **kwargs):
        kwargs['table'] = Meetings.objects.order_by('-id')
        return super().get_context_data(**kwargs)


class ItemFormView(LoginRequiredMixin, FormView):
    login_url = reverse_lazy('login')
    template_name = 'main/index.html'
    success_url = reverse_lazy('inventory')
    form_class = TableForm

    def form_valid(self, form):
        for _ in range(form.cleaned_data['extra']):
            object = form.save(commit=False)
            object.pk = None  # yes, that is hack
            object.userID = self.request.user
            object.value = object.sellprice - object.price
            object.save()
        return super().form_valid(form)


class MeetingsFormView(LoginRequiredMixin, FormView):
    login_url = reverse_lazy('login')
    template_name = 'main/index.html'
    success_url = reverse_lazy('inventory')
    form_class = MeetingForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.userID = self.request.user
        self.object.item_id = self.kwargs['pk']
        self.object.save()
        return super().form_valid(form)


class GoodMeetingDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'login'
    model = Meetings
    template_name = 'main/index.html'
    success_url = reverse_lazy('meetings')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user != self.object.userID:
            return self.handle_no_permission()
        success_url = self.get_success_url()
        item = Table.objects.get(id=self.object.item_id)
        item.datesell = self.object.datemeeting
        item.sellprice = self.object.sellprice
        item.value = item.sellprice - item.price
        item.save()
        self.object.delete()
        return HttpResponseRedirect(success_url)


class MeetingDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'login'
    model = Meetings
    template_name = 'main/index.html'
    success_url = reverse_lazy('meetings')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user != self.object.userID:
            return self.handle_no_permission()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)


# class ItemCreateView(LoginRequiredMixin, CreateView):
#     login_url = reverse_lazy('login')
#     model = Table
#     template_name = 'main/index.html'
#     form_class = TableForm
#     success_url = reverse_lazy('inventory')
#
#     def form_valid(self, form):
#         self.object = form.save(commit=False)
#         self.object.userID = self.request.user
#         self.object.value = self.object.sellprice - self.object.price
#         self.object.save()
#         return super().form_valid(form)
#
#     def get_context_data(self, **kwargs):
#         last_year = timezone.now().date() - timedelta(days=365)
#         last_month = timezone.now().date() - timedelta(days=30)
#         some_day_last_week = timezone.now().date() - timedelta(days=7)
#         year_sum = Table.objects.filter(datesell__gte=last_year, userID=self.request.user).aggregate(Sum('sellprice'))
#         if year_sum['sellprice__sum'] is None:
#             year_sum['sellprice__sum'] = 0
#         week_sum = Table.objects.filter(datesell__gte=some_day_last_week, userID=self.request.user).aggregate(
#             Sum('sellprice'))
#         if week_sum['sellprice__sum'] is None:
#             week_sum['sellprice__sum'] = 0
#         month_sum = Table.objects.filter(datesell__gte=last_month, userID=self.request.user).aggregate(Sum('sellprice'))
#         if month_sum['sellprice__sum'] is None:
#             month_sum['sellprice__sum'] = 0
#         year_sum_b = Table.objects.filter(datebuy__gte=last_year, userID=self.request.user).aggregate(Sum('price'))
#         if year_sum_b['price__sum'] is None:
#             year_sum_b['price__sum'] = 0
#         week_sum_b = Table.objects.filter(datebuy__gte=some_day_last_week, userID=self.request.user).aggregate(
#             Sum('price'))
#         if week_sum_b['price__sum'] is None:
#             week_sum_b['price__sum'] = 0
#         month_sum_b = Table.objects.filter(datebuy__gte=last_month, userID=self.request.user).aggregate(Sum('price'))
#         if month_sum_b['price__sum'] is None:
#             month_sum_b['price__sum'] = 0
#         year_value = year_sum['sellprice__sum'] - year_sum_b['price__sum']
#         month_value = month_sum['sellprice__sum'] - month_sum_b['price__sum']
#         week_value = week_sum['sellprice__sum'] - week_sum_b['price__sum']
#         dic_sum = Table.objects.filter(userID=self.request.user).aggregate(Sum('value'))
#         if dic_sum['value__sum'] is None:
#             dic_sum['value__sum'] = 0
#
#         kwargs['year_value'] = year_value
#         kwargs['month_value'] = month_value
#         kwargs['week_value'] = week_value
#         kwargs['sum'] = dic_sum['value__sum']
#         kwargs['table'] = Table.objects.order_by('-id')
#         print(kwargs)
#         return super().get_context_data(**kwargs)


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
    redirect_authenticated_user = 'inventory'
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
    next_page = reverse_lazy('login')


class DeliveryView(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    template_name = 'main/delivery.html'


class StatisticView(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    template_name = 'main/statistic.html'

    def get_context_data(self, **kwargs):
        labels = []
        sellprice = []
        year_labels = []
        year_income = []
        month_labels = []
        month_income = []
        week_labels = []
        week_income = []
        last_year = timezone.now().date() - timedelta(days=365)
        last_month = timezone.now().date() - timedelta(days=30)
        last_week = timezone.now().date() - timedelta(days=7)
        q = Table.objects.filter(datesell__isnull=False, userID=self.request.user).order_by('datesell')
        q_year = Table.objects.filter(datesell__gte=last_year, userID=self.request.user).order_by('datesell')
        q_month = Table.objects.filter(datesell__gte=last_month, userID=self.request.user).order_by('datesell')
        q_week = Table.objects.filter(datesell__gte=last_week, userID=self.request.user).order_by('datesell')
        for i in q:
            if i.datesell.strftime('%d.%m.%Y') not in labels:
                labels.append(i.datesell.strftime('%d.%m.%Y'))
                sellprice.append(float(i.sellprice - i.price - i.anyprice))
            else:
                sellprice[labels.index(i.datesell.strftime('%d.%m.%Y'))] += float(i.sellprice - i.price - i.anyprice)
        for i in q_year:
            if i.datesell.strftime('%B') not in labels:
                year_labels.append(i.datesell.strftime('%B'))
                year_income.append(float(i.sellprice - i.price - i.anyprice))
            else:
                year_labels[labels.index(i.datesell.strftime('%B'))] += float(i.sellprice - i.price - i.anyprice)
        for i in q_month:
            if i.datesell.strftime('%d %B') not in labels:
                month_labels.append(i.datesell.strftime('%d %B'))
                month_income.append(float(i.sellprice - i.price - i.anyprice))
            else:
                month_labels[labels.index(i.datesell.strftime('%d %B'))] += float(i.sellprice - i.price - i.anyprice)
        for i in q_week:
            if i.datesell.strftime('%d %B') not in labels:
                week_labels.append(i.datesell.strftime('%d %B'))
                week_income.append(float(i.sellprice - i.price - i.anyprice))
            else:
                week_labels[labels.index(i.datesell.strftime('%d %B'))] += float(i.sellprice - i.price - i.anyprice)

        print(labels, sellprice, q)
        kwargs['week_dates'] = week_labels
        kwargs['week_income'] = week_income
        kwargs['month_dates'] = month_labels
        kwargs['month_income'] = month_income
        kwargs['year_dates'] = year_labels
        kwargs['year_income'] = year_income
        kwargs['income'] = sellprice
        kwargs['dates'] = labels
        return super().get_context_data(**kwargs)
