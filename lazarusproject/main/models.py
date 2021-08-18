from django.db import models

# Create your models here.

US_SIZES = (
        ('0', 'NO SIZE'),
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


class Table(models.Model):
    title = models.CharField('Name', max_length=100)
    datebuy = models.DateField(null=True)
    datesell = models.DateField(blank=True, null=True)
    price = models.FloatField()
    sellprice = models.FloatField(blank=True, null=True)
    anyprice = models.FloatField(blank=True, null=True)
    value = models.FloatField(blank=True, null=True, editable=False)
    size = models.CharField('Size', max_length=5, choices=US_SIZES, default='')
    notes = models.CharField('Notes', max_length=255, blank=True, default='')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Sneaker'
        verbose_name_plural = 'Sneakers'
