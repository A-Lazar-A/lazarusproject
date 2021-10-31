# Generated by Django 3.2.6 on 2021-10-31 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0025_auto_20211018_2031'),
    ]

    operations = [
        migrations.AddField(
            model_name='table',
            name='currency',
            field=models.CharField(choices=[('rub', '₽'), ('usd', '$'), ('eur', '€'), ('sol', 'SOL'), ('eth', 'ETH')], default='0', max_length=10, verbose_name='Currency'),
        ),
    ]
