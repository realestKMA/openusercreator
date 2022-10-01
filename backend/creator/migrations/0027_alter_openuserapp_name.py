# Generated by Django 4.0.4 on 2022-10-01 15:41

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creator', '0026_alter_openuserapp_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='openuserapp',
            name='name',
            field=models.CharField(help_text='The name of this Openuser profile.', max_length=20, validators=[django.core.validators.RegexValidator(message='Must begin and end with a letter. Maximum of 2 whitespaces', regex='^[a-zA-Z]([\\w ]*[a-zA-Z]*)?$'), django.core.validators.MinLengthValidator(limit_value=4)], verbose_name='Name'),
        ),
    ]
