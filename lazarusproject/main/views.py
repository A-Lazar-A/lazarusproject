from binance.spot import Spot
from decimal import Decimal

from datetime import timedelta

from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import DeleteView, UpdateView, CreateView, TemplateView, FormView, ListView

from .forms import TableForm, AuthUserForm, SignUpForm, MeetingForm, AddItemForMeetingForm, TableSoldForm, TableEditForm
from .models import Table, Meetings, PotentialSellPrice

from datetime import date


class MainTemplateView(LoginRequiredMixin, TemplateView):
    """
    Отображает страницу инвентаря пользователя

    **Загрузка контекста страницы**

        ''form''
            Форма для добавления предмета в инвентарь
        ''edit_form''
            Форма для редактирования предмета
        ''sold_form''
            Форма для записи данных если предмет был продан
        ''meetings_form''
            Форма для назначения встречи
        ''add_item_to_meeting_form''
            Форма для добавления предмета на встречу
        ''year_value''
            Прибыль за год
        ''month_value''
            Прибыль за месяц
        ''week_value''
            Прибыль за неделю
        ''sum''
            Прибыль за все время
        ''table''
            Предметы пользователя
        ''meetings''
            Существуют ли встречи у пользователя


    **Шаблон:**

    :template:`templates/main/index.html`

    """

    login_url = reverse_lazy('login')
    template_name = 'main/index.html'
    model = Table

    def get_context_data(self, *, object_list=None, **kwargs):
        """
         **Загрузка контекста страницы**

        ''form''
            Форма для добавления предмета в инвентарь
        ''edit_form''
            Форма для редактирования предмета
        ''sold_form''
            Форма для записи данных если предмет был продан
        ''meetings_form''
            Форма для назначения встречи
        ''add_item_to_meeting_form''
            Форма для добавления предмета на встречу
        ''year_value''
            Прибыль за год
        ''month_value''
            Прибыль за месяц
        ''week_value''
            Прибыль за неделю
        ''sum''
            Прибыль за все время
        ''table''
            Предметы пользователя
        ''meetings''
            Существуют ли встречи у пользователя

        :param object_list:
        :param kwargs:
        :return:
        """
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
        year_sum_any = Table.objects.filter(datesell__gte=last_year, userID=self.request.user).aggregate(Sum('anyprice'))
        year_sum_any['anyprice__sum'] = None or year_sum_any['anyprice__sum'] or 0
        week_sum_any = Table.objects.filter(datesell__gte=some_day_last_week, userID=self.request.user).aggregate(
            Sum('anyprice'))
        week_sum_any['anyprice__sum'] = None or week_sum_any['anyprice__sum'] or 0
        month_sum_any = Table.objects.filter(datesell__gte=last_month, userID=self.request.user).aggregate(Sum('anyprice'))
        month_sum_any['anyprice__sum'] = None or month_sum_any['anyprice__sum'] or 0
        year_sum_b = Table.objects.filter(datebuy__gte=last_year, userID=self.request.user).aggregate(Sum('price'))
        year_sum_b['price__sum'] = None or year_sum_b['price__sum'] or 0
        week_sum_b = Table.objects.filter(datebuy__gte=some_day_last_week, userID=self.request.user).aggregate(
            Sum('price'))
        week_sum_b['price__sum'] = None or week_sum_b['price__sum'] or 0
        month_sum_b = Table.objects.filter(datebuy__gte=last_month, userID=self.request.user).aggregate(Sum('price'))
        month_sum_b['price__sum'] = None or month_sum_b['price__sum'] or 0
        year_value = year_sum['sellprice__sum'] - year_sum_b['price__sum'] - year_sum_any['anyprice__sum']
        month_value = month_sum['sellprice__sum'] - month_sum_b['price__sum'] - month_sum_any['anyprice__sum']
        week_value = week_sum['sellprice__sum'] - week_sum_b['price__sum'] - week_sum_any['anyprice__sum']
        dic_sum = Table.objects.filter(userID=self.request.user).aggregate(Sum('value'))
        dic_sum['value__sum'] = None or dic_sum['value__sum'] or 0
        item_form = TableForm(self.request.GET or None, initial={'datebuy': date.today().strftime("%Y-%m-%d")})
        item_edit_form = TableEditForm(self.request.GET or None)
        meetings_form = MeetingForm(self.request.GET or None)
        sold_form = TableSoldForm(self.request.GET or None, initial={'datesell': date.today().strftime("%Y-%m-%d")})
        add_item_to_meeting_form = AddItemForMeetingForm(self.request.GET or None, username=self.request.user)
        kwargs['form'] = item_form
        kwargs['edit_form'] = item_edit_form
        kwargs['sold_form'] = sold_form
        kwargs['meetings_form'] = meetings_form
        kwargs['add_item_to_meeting_form'] = add_item_to_meeting_form
        kwargs['year_value'] = year_value
        kwargs['month_value'] = month_value
        kwargs['week_value'] = week_value
        kwargs['sum'] = dic_sum['value__sum']
        kwargs['table'] = Table.objects.filter(userID=self.request.user).order_by('-id')
        kwargs['meetings'] = Meetings.objects.filter(userID=self.request.user).exists()
        return super().get_context_data(**kwargs)



class MeetingsListView(LoginRequiredMixin, ListView):
    """
    Отображает страницу встреч

    **Загрузка контекста страницы**

        ''table''
             Встречи пользователя

    **Шаблон:**

    :template:`templates/main/meetings.html`

    """
    login_url = reverse_lazy('login')
    template_name = 'main/meetings.html'
    model = Meetings

    def get_context_data(self, **kwargs):
        kwargs['table'] = Meetings.objects.filter(userID=self.request.user).order_by('-id')
        return super().get_context_data(**kwargs)


class ItemFormView(LoginRequiredMixin, FormView):

    """
    Добавление предмета в инвентарь
    """

    login_url = reverse_lazy('login')
    template_name = 'main/index.html'
    success_url = reverse_lazy('inventory')
    form_class = TableForm

    def form_valid(self, form):
        for _ in range(form.cleaned_data['extra']):
            object = form.save(commit=False)
            object.price = object.currencyprice
            object.sellprice = object.currencysellprice
            if object.currencysell != '₽':
                client = Spot(key='GvmucOiF2eSkzMoQ7J8hBe4ry9nY6UYs5SvsPxcHKW5SmcxDwHZhuoTkTLcwcNaE',
                              secret='MlNv5KlRnS6mHtRdQns75zJv1FQjfVs2qNj9ZAlENfKvas5BAcvNtq8bOea2fhMP')
                if object.currencysell == 'BUSD':
                    object.sellprice *= Decimal(client.ticker_price('BUSDRUB')['price'])
                elif object.currencysell == 'SOL':
                    object.sellprice *= Decimal(client.ticker_price('SOLRUB')['price'])
                elif object.currencysell == 'ETH':
                    object.sellprice *= Decimal(client.ticker_price('ETHRUB')['price'])

            if object.currencybuy != '₽':
                client = Spot(key='GvmucOiF2eSkzMoQ7J8hBe4ry9nY6UYs5SvsPxcHKW5SmcxDwHZhuoTkTLcwcNaE',
                              secret='MlNv5KlRnS6mHtRdQns75zJv1FQjfVs2qNj9ZAlENfKvas5BAcvNtq8bOea2fhMP')
                if object.currencybuy == 'BUSD':
                    object.price *= Decimal(client.ticker_price('BUSDRUB')['price'])
                elif object.currencybuy == 'SOL':
                    object.price *= Decimal(client.ticker_price('SOLRUB')['price'])
                elif object.currencybuy == 'ETH':
                    object.price *= Decimal(client.ticker_price('ETHRUB')['price'])
            object.pk = None
            object.userID = self.request.user
            object.value = object.sellprice - object.price - object.anyprice
            object.save()
        return super().form_valid(form)


class MeetingsFormView(LoginRequiredMixin, FormView):
    """
    Добавление встречи
    """

    login_url = reverse_lazy('login')
    template_name = 'main/index.html'
    success_url = reverse_lazy('inventory')
    form_class = MeetingForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.userID = self.request.user
        item = Table.objects.get(id=self.kwargs['pk'])
        price = form.cleaned_data['price']
        currency = form.cleaned_data['currency']

        if currency != '₽':
            client = Spot(key='GvmucOiF2eSkzMoQ7J8hBe4ry9nY6UYs5SvsPxcHKW5SmcxDwHZhuoTkTLcwcNaE',
                          secret='MlNv5KlRnS6mHtRdQns75zJv1FQjfVs2qNj9ZAlENfKvas5BAcvNtq8bOea2fhMP')
            if currency == 'BUSD':
                price *= Decimal(client.ticker_price('BUSDRUB')['price'])
            elif currency == 'SOL':
                price *= Decimal(client.ticker_price('SOLRUB')['price'])
            elif currency == 'ETH':
                price *= Decimal(client.ticker_price('ETHRUB')['price'])
        self.object.sellpricesum = price
        self.object.save()
        item.meet = self.object
        pps = PotentialSellPrice(userID=self.request.user, potentialprice=self.object.sellpricesum)
        pps.save()
        item.possibleprice = pps
        item.save()
        return super().form_valid(form)


class AddItemForMeetingFormView(LoginRequiredMixin, UpdateView):
    """
    Добавление предмета к встрече
    """
    login_url = reverse_lazy('login')
    template_name = 'main/index.html'
    success_url = reverse_lazy('inventory')
    form_class = AddItemForMeetingForm
    model = Table

    def get_form_kwargs(self):
        kwargs = super(AddItemForMeetingFormView, self).get_form_kwargs()
        kwargs['username'] = self.request.user
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        price = form.cleaned_data["price"]
        currency = form.cleaned_data['currency']
        if currency != '₽':
            client = Spot(key='GvmucOiF2eSkzMoQ7J8hBe4ry9nY6UYs5SvsPxcHKW5SmcxDwHZhuoTkTLcwcNaE',
                          secret='MlNv5KlRnS6mHtRdQns75zJv1FQjfVs2qNj9ZAlENfKvas5BAcvNtq8bOea2fhMP')
            if currency == 'BUSD':
                price *= Decimal(client.ticker_price('BUSDRUB')['price'])
            elif currency == 'SOL':
                price *= Decimal(client.ticker_price('SOLRUB')['price'])
            elif currency == 'ETH':
                price *= Decimal(client.ticker_price('ETHRUB')['price'])
        pps = PotentialSellPrice(userID=self.request.user, potentialprice=price)
        pps.save()
        self.object.possibleprice = pps
        self.object.meet.sellpricesum += price
        self.object.meet.save()
        self.object.save()

        return super().form_valid(form)


class GoodMeetingDeleteView(LoginRequiredMixin, DeleteView):
    """
    Удаление встречи при успешной продаже
    """
    login_url = 'login'
    model = Meetings
    template_name = 'main/index.html'
    success_url = reverse_lazy('meetings')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user != self.object.userID:
            return self.handle_no_permission()
        success_url = self.get_success_url()
        items = Table.objects.filter(meet=self.object)
        for item in items:
            item.datesell = self.object.datemeeting
            item.currencysellprice = item.possibleprice.potentialprice
            item.value = item.currencysellprice - item.price - item.anyprice
            item.possibleprice.delete()
            item.possibleprice = None
            item.save()
        self.object.delete()
        return HttpResponseRedirect(success_url)


class MeetingDeleteView(LoginRequiredMixin, DeleteView):
    """
    Удаление встречи
    """

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



class ItemDeleteView(LoginRequiredMixin, DeleteView):
    """
    Удаление предмета
    """
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
    """
    Изменение предмета
    """

    login_url = 'login'
    model = Table
    template_name = 'main/index.html'
    form_class = TableEditForm
    success_url = reverse_lazy('inventory')

    def form_valid(self, form):
        object = form.save(commit=False)
        object.price = object.currencyprice
        object.sellprice = object.currencysellprice
        if object.currencysell != '₽':
            client = Spot(key='GvmucOiF2eSkzMoQ7J8hBe4ry9nY6UYs5SvsPxcHKW5SmcxDwHZhuoTkTLcwcNaE',
                          secret='MlNv5KlRnS6mHtRdQns75zJv1FQjfVs2qNj9ZAlENfKvas5BAcvNtq8bOea2fhMP')
            if object.currencysell == 'BUSD':
                object.sellprice *= Decimal(client.ticker_price('BUSDRUB')['price'])

            elif object.currencysell == 'SOL':
                object.sellprice *= Decimal(client.ticker_price('SOLRUB')['price'])
            elif object.currencysell == 'ETH':
                object.sellprice *= Decimal(client.ticker_price('ETHRUB')['price'])

        if object.currencybuy != '₽':
            client = Spot(key='GvmucOiF2eSkzMoQ7J8hBe4ry9nY6UYs5SvsPxcHKW5SmcxDwHZhuoTkTLcwcNaE',
                          secret='MlNv5KlRnS6mHtRdQns75zJv1FQjfVs2qNj9ZAlENfKvas5BAcvNtq8bOea2fhMP')
            if object.currencybuy == 'BUSD':
                object.price *= Decimal(client.ticker_price('BUSDRUB')['price'])
            elif object.currencybuy == 'SOL':
                object.price *= Decimal(client.ticker_price('SOLRUB')['price'])
            elif object.currencybuy == 'ETH':
                object.price *= Decimal(client.ticker_price('ETHRUB')['price'])
        object.userID = self.request.user
        object.value = object.sellprice - object.price - object.anyprice
        object.save()
        return super().form_valid(form)


class ItemSoldView(LoginRequiredMixin, UpdateView):
    """
    Редактирование предмета если он был продан
    """
    login_url = 'login'
    model = Table
    template_name = 'main/index.html'
    form_class = TableSoldForm
    success_url = reverse_lazy('inventory')

    def form_valid(self, form):
        object = form.save(commit=False)
        object.sellprice = object.currencysellprice
        if object.currencysell != '₽':
            client = Spot(key='GvmucOiF2eSkzMoQ7J8hBe4ry9nY6UYs5SvsPxcHKW5SmcxDwHZhuoTkTLcwcNaE',
                          secret='MlNv5KlRnS6mHtRdQns75zJv1FQjfVs2qNj9ZAlENfKvas5BAcvNtq8bOea2fhMP')
            if object.currencysell == 'BUSD':
                object.sellprice *= Decimal(client.ticker_price('BUSDRUB')['price'])
            elif object.currencysell == 'SOL':
                object.sellprice *= Decimal(client.ticker_price('SOLRUB')['price'])
            elif object.currencysell == 'ETH':
                object.sellprice *= Decimal(client.ticker_price('ETHRUB')['price'])
        object.userID = self.request.user
        self.object.value = self.object.sellprice - self.object.price - self.object.anyprice
        self.object.save()
        return super().form_valid(form)


class UserLoginView(LoginView):
    """
    Отображение для входа пользователя в аккаунт
    """

    redirect_authenticated_user = 'inventory'
    model = User
    template_name = 'main/login.html'
    form_class = AuthUserForm
    success_url = reverse_lazy('inventory')

    def get_success_url(self):
        return self.success_url


class UserRegisterView(CreateView):
    """
    Отображение для регистрации нового аккаунта пользователя
    """
    model = User
    template_name = 'main/sign-up.html'
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
    """
    Выход пользователя из аккаунта
    """
    next_page = reverse_lazy('login')


class DeliveryView(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    template_name = 'main/delivery.html'


class StatisticView(LoginRequiredMixin, TemplateView):
    """
    Отображение статистики

    **Загрузка контекста страницы**

        ''week_dates''
            Дни с прибылью за последнюю неделю
        ''week_income''
            Прибыль на каждый день из 'week_dates'
        ''month_dates''
            Дни с прибылью за последний месяц
        ''month_income''
            Прибыль на каждый день из 'month_dates'
        ''year_dates''
            Месяцы с прибылью за последний год
        ''year_income''
            Прибыль на каждый месяц из 'year_dates'
        ''income''
            Дни с прибылью за все время
        ''dates''
            Прибыль на каждый дни из 'income'

    """
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
            if i.datesell.strftime('%B') not in year_labels:
                year_labels.append(i.datesell.strftime('%B'))
                year_income.append(float(i.sellprice - i.price - i.anyprice))
            else:
                year_income[year_labels.index(i.datesell.strftime('%B'))] += float(i.sellprice - i.price - i.anyprice)
        for i in q_month:
            if i.datesell.strftime('%d %B') not in month_labels:
                month_labels.append(i.datesell.strftime('%d %B'))
                month_income.append(float(i.sellprice - i.price - i.anyprice))
            else:
                month_income[month_labels.index(i.datesell.strftime('%d %B'))] += float(i.sellprice - i.price - i.anyprice)
        for i in q_week:
            if i.datesell.strftime('%d %B') not in week_labels:
                week_labels.append(i.datesell.strftime('%d %B'))
                week_income.append(float(i.sellprice - i.price - i.anyprice))
            else:
                week_income[week_labels.index(i.datesell.strftime('%d %B'))] += float(i.sellprice - i.price - i.anyprice)

        kwargs['week_dates'] = week_labels
        kwargs['week_income'] = week_income
        kwargs['month_dates'] = month_labels
        kwargs['month_income'] = month_income
        kwargs['year_dates'] = year_labels
        kwargs['year_income'] = year_income
        kwargs['income'] = sellprice
        kwargs['dates'] = labels
        return super().get_context_data(**kwargs)
