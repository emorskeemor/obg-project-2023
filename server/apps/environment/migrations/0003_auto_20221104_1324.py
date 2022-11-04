# Generated by Django 3.2.15 on 2022-11-04 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0001_initial'),
        ('environment', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='generationsettings',
            name='email_domain',
            field=models.CharField(blank=True, help_text='student email domain name must match this domain', max_length=50, null=True, verbose_name='email domain match'),
        ),
        migrations.AlterField(
            model_name='avalilableoptionchoices',
            name='options',
            field=models.ManyToManyField(related_name='available_option_choices', through='environment.AvailableOption', to='students.Option', verbose_name='available options'),
        ),
        migrations.AlterUniqueTogether(
            name='availableoption',
            unique_together={('option', 'option_choices')},
        ),
    ]
