# Generated by Django 3.2.6 on 2021-10-31 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0029_auto_20211031_1648'),
    ]

    operations = [
        migrations.AlterField(
            model_name='table',
            name='value',
            field=models.DecimalField(blank=True, decimal_places=2, editable=False, max_digits=19, null=True),
        ),
    ]