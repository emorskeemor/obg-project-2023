# Generated by Django 3.2.15 on 2023-03-19 15:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='option',
            name='requirements',
        ),
        migrations.RemoveField(
            model_name='option',
            name='slug',
        ),
    ]
