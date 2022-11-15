# Generated by Django 3.2.15 on 2022-11-15 13:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('environment', '0009_auto_20221114_1709'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='options_using',
        ),
        migrations.AddField(
            model_name='avalilableoptionchoices',
            name='room',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='available_option_choices', to='environment.room'),
        ),
    ]
