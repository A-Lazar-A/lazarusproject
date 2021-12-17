from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Create your models here.

CURRENCY_CHOICES = (
    ('₽', '₽'),
    ('BUSD', 'BUSD'),
    ('SOL', 'SOL'),
    ('ETH', 'ETH')
)

US_SIZES = (
    ('NO SIZE', 'NO SIZE'),
    ('3', '3 US'),
    ('3.5', '3.5 US'),
    ('4', '4 US'),
    ('4.5', '4.5 US'),
    ('5', '5 US'),
    ('5.5', '5.5 US'),
    ('6', '6 US'),
    ('6.5', '6.5 US'),
    ('7', '7 US'),
    ('7.5', '7.5 US'),
    ('8', '8 US'),
    ('8.5', '8.5 US'),
    ('9', '9 US'),
    ('9.5', '9.5 US'),
    ('10', '10 US'),
    ('10.5', '10.5 US'),
    ('11', '11 US'),
    ('11.5', '11.5 US'),
    ('12', '12 US'),
    ('12.5', '12.5 US'),
    ('13', '13 US'),
    ('13.5', '13.5 US'),
    ('14', '14 US'),
    ('14.5', '14.5 US'),
    ('15', '15 US')
)


class Meetings(models.Model):
    """
    Модель встречи
    """
    userID = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User ID', blank=True, null=True)
    title = models.CharField('Название', max_length=100)
    datemeeting = models.DateTimeField('Дата встречи', null=True)
    sellpricesum = models.DecimalField('Общая сумма вещей на продажу', blank=False, null=True, default=0, max_digits=19,
                                       decimal_places=2)
    notes = models.TextField('Заметки', blank=True, default='')

    def get_item(self):
        return Table.objects.filter(meet=self)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return '/inventory/'

    class Meta:
        verbose_name = 'Meeting'
        verbose_name_plural = 'Meetings'


class PotentialSellPrice(models.Model):
    """
    Модель потенциальной цены продажи предмета
    """
    userID = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User ID', blank=True, null=True)
    potentialprice = models.DecimalField(max_digits=19, decimal_places=2)

    def __str__(self):
        return str(self.potentialprice)

    def get_absolute_url(self):
        return '/inventory/'

    class Meta:
        verbose_name = 'Potential Sell Price'
        verbose_name_plural = 'Potential Sell Prices'


class Table(models.Model):
    """
    Модель предмета
    """
    userID = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User ID', blank=True, null=True)
    title = models.CharField('Название', max_length=100)
    datebuy = models.DateField('Дата покупки', null=True)
    datesell = models.DateField('Дата продажи', blank=True, null=True)
    price = models.DecimalField('Цена покупки', max_digits=19, decimal_places=2, default=0)
    sellprice = models.DecimalField('Цена продажи', blank=False, null=False, default=0, max_digits=19, decimal_places=2)
    anyprice = models.DecimalField('Доп расходы', blank=False, null=False, default=0, max_digits=19, decimal_places=2)
    value = models.DecimalField('Прибыль', blank=True, null=True, editable=False, max_digits=19, decimal_places=2)
    currencysellprice = models.DecimalField('Цена продажи в валюте', blank=False, null=False, default=0, max_digits=19,
                                            decimal_places=4)
    currencyprice = models.DecimalField('Цена покупки в валюте', blank=False, null=False, default=0, max_digits=19,
                                        decimal_places=4)
    currencysell = models.CharField('Валюта продажи', max_length=10, choices=CURRENCY_CHOICES, default='rub')
    currencybuy = models.CharField('Валюта покупки', max_length=10, choices=CURRENCY_CHOICES, default='rub')
    size = models.CharField('Размер', max_length=10, choices=US_SIZES, default='NO SIZE')
    notes = models.TextField('Заметки', blank=True, default='')
    meet = models.ForeignKey(Meetings, on_delete=models.SET_NULL, null=True)
    possibleprice = models.OneToOneField(PotentialSellPrice, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return '/inventory/'

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'
