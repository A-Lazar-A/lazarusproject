# Generated by Django 3.2.6 on 2021-10-15 16:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_remove_meetings_iditem'),
    ]

    operations = [
        migrations.AddField(
            model_name='table',
            name='meet',
            field=models.ForeignKey(default=40, on_delete=django.db.models.deletion.SET_DEFAULT, to='main.meetings'),
        ),
    ]