# Generated by Django 3.2.6 on 2021-09-17 19:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_meetings_item_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meetings',
            name='item_id',
        ),
    ]
