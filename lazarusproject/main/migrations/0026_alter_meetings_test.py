# Generated by Django 3.2.6 on 2021-09-17 19:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0025_auto_20210917_1926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meetings',
            name='test',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.table'),
        ),
    ]
