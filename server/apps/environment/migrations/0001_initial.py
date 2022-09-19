# Generated by Django 3.2.15 on 2022-09-19 19:46

import apps.environment.models.rooms
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default=apps.environment.models.rooms.generate_room_code, max_length=8, verbose_name='room code')),
                ('domain', models.CharField(max_length=40, verbose_name='domain name')),
                ('slug', models.SlugField(blank=True, max_length=250)),
                ('public', models.BooleanField(default=False, verbose_name='room is public')),
                ('admin', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to=settings.AUTH_USER_MODEL, verbose_name='create by')),
            ],
        ),
    ]
