# Generated by Django 3.2.6 on 2021-10-31 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0030_alter_table_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='table',
            name='anyprice',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=19),
        ),
    ]