# Generated by Django 3.2.6 on 2021-09-17 19:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_alter_table_size'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meetings',
            name='iditem',
        ),
    ]
