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
    userID = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User ID', blank=True, null=True)
    title = models.CharField('Name', max_length=100)
    datemeeting = models.DateTimeField(null=True)
    sellpricesum = models.DecimalField(blank=False, null=True, default=0, max_digits=19, decimal_places=2)
    notes = models.TextField('Notes', blank=True, default='')

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
    userID = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User ID', blank=True, null=True)
    title = models.CharField('Name', max_length=100)
    datebuy = models.DateField(null=True)
    datesell = models.DateField(blank=True, null=True)
    price = models.DecimalField(max_digits=19, decimal_places=2, default=0)
    sellprice = models.DecimalField(blank=False, null=False, default=0, max_digits=19, decimal_places=2)
    anyprice = models.DecimalField(blank=False, null=False, default=0, max_digits=19, decimal_places=2)
    value = models.DecimalField(blank=True, null=True, editable=False, max_digits=19, decimal_places=2)
    currencysellprice = models.DecimalField(blank=False, null=False, default=0, max_digits=19, decimal_places=4)
    currencyprice = models.DecimalField(blank=False, null=False, default=0, max_digits=19, decimal_places=4)
    currencysell = models.CharField('CurrencySell', max_length=10, choices=CURRENCY_CHOICES, default='rub')
    currencybuy = models.CharField('CurrencyBuy', max_length=10, choices=CURRENCY_CHOICES, default='rub')
    size = models.CharField('Size', max_length=10, choices=US_SIZES, default='NO SIZE')
    notes = models.TextField('Notes', blank=True, default='')
    meet = models.ForeignKey(Meetings, on_delete=models.SET_NULL, null=True)
    possibleprice = models.OneToOneField(PotentialSellPrice, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return '/inventory/'

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'





