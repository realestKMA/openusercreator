# Generated by Django 4.0.4 on 2022-05-28 10:11

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creator', '0006_alter_appuser_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appuser',
            name='username',
            field=models.CharField(error_messages={'unique': 'This username is not available'}, max_length=20, unique=True, validators=[django.core.validators.RegexValidator(inverse_match=True, message='Username can only contain letters, numbers and underscore', regex='\\W'), django.core.validators.MinLengthValidator(limit_value=4)], verbose_name='Username'),
        ),
    ]
