# Generated by Django 3.2.6 on 2021-10-18 17:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0023_alter_table_meet'),
    ]

    operations = [
        migrations.CreateModel(
            name='PotentialSellPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('potentialprice', models.DecimalField(decimal_places=2, max_digits=19)),
                ('userID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User ID')),
            ],
            options={
                'verbose_name': 'Potential Sell Price',
                'verbose_name_plural': 'Potential Sell Prices',
            },
        ),
        migrations.AddField(
            model_name='table',
            name='possibleprice',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.potentialsellprice'),
        ),
    ]