# Generated by Django 3.2.6 on 2021-09-10 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_auto_20210910_1259'),
    ]

    operations = [
        migrations.AddField(
            model_name='meetings',
            name='iditem',
            field=models.IntegerField(null=True),
        ),
    ]
