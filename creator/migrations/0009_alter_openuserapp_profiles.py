# Generated by Django 4.0.4 on 2022-09-01 11:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creator', '0008_rename_openuser_openuserapp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='openuserapp',
            name='profiles',
            field=models.IntegerField(default=2, help_text='Number of openuser profiles to create, default is 2', validators=[django.core.validators.MaxValueValidator(limit_value=25), django.core.validators.MinValueValidator(limit_value=1)], verbose_name='Profiles'),
        ),
    ]
