# Generated by Django 3.2.15 on 2022-11-13 01:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('environment', '0006_alter_room_options_using'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generationsettings',
            name='room',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='settings', to='environment.room', verbose_name='room connected to'),
        ),
    ]
