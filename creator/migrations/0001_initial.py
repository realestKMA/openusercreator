# Generated by Django 4.0.4 on 2022-07-11 09:23

import creator.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.constraints
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppUser',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.BigAutoField(editable=False, primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('uid', models.CharField(default=creator.models.get_random_int, editable=False, max_length=50, unique=True, verbose_name='USER ID')),
                ('password', models.CharField(max_length=128, validators=[django.core.validators.MinLengthValidator(limit_value=8), django.core.validators.RegexValidator(inverse_match=True, message='Password cannot contain spaces', regex='\\s')], verbose_name='Password')),
                ('username', models.CharField(error_messages={'unique': 'This username is not available'}, max_length=15, unique=True, validators=[django.core.validators.MinLengthValidator(limit_value=4), django.core.validators.RegexValidator(inverse_match=True, message='Username can only contain letters, numbers and underscore', regex='\\W')], verbose_name='Username')),
                ('first_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='First Name')),
                ('last_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Last Name')),
                ('other_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Other Name')),
                ('email', models.EmailField(error_messages={'unique': 'This email address belongs to another account'}, max_length=255, unique=True, verbose_name='Email Address')),
                ('is_verified', models.BooleanField(default=False, help_text='Designates whether this user has verified their email address.', verbose_name='Verified User')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'ordering': ['-date_joined'],
            },
        ),
        migrations.CreateModel(
            name='Openuser',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='App unique ID', primary_key=True, serialize=False, unique=True, verbose_name='App ID')),
                ('endpoint', models.URLField(blank=True, help_text='Url endpoint for your openuser profiles', max_length=255, null=True, verbose_name='Endpoint')),
                ('name', models.CharField(help_text='The name of this Openuser profile. Spaces are replaces with underscores', max_length=20, validators=[django.core.validators.RegexValidator(message='Must begin and end with a letter. And can only contain letters, numbers and hyphens', regex='^[a-zA-Z]([\\w -]*[a-zA-Z])?$'), django.core.validators.MinLengthValidator(limit_value=4)], verbose_name='Name')),
                ('profiles', models.IntegerField(default=5, help_text='Number of openuser profiles to create, defaul is 5', validators=[django.core.validators.MaxValueValidator(limit_value=25), django.core.validators.MinValueValidator(limit_value=1)], verbose_name='Profiles')),
                ('profile_password', models.CharField(default='p@ssw0rd', help_text='The password to use for all profiles', max_length=15, validators=[django.core.validators.RegexValidator(inverse_match=True, message='Profile password cannot contain spaces', regex='\\s')], verbose_name='Profile password')),
                ('date_created', models.DateTimeField(auto_now_add=True, help_text='The date and time this Openuser profile was created', verbose_name='Date Created')),
                ('last_updated', models.DateTimeField(auto_now=True, help_text='The last time this Openuser profile was updated', verbose_name='Last Updated')),
                ('status', models.CharField(choices=[('Creating', 'Creating'), ('Created', 'Created')], default='Creating', help_text='Openuser status', max_length=50, verbose_name='Status')),
                ('creator', models.ForeignKey(help_text='The Appuser who owns this Openuser profiles', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='creator')),
            ],
            options={
                'ordering': ['-date_created'],
            },
        ),
        migrations.AddConstraint(
            model_name='openuser',
            constraint=models.UniqueConstraint(deferrable=django.db.models.constraints.Deferrable['DEFERRED'], fields=('creator', 'name'), name='unique_openuser'),
        ),
        migrations.AddConstraint(
            model_name='appuser',
            constraint=models.CheckConstraint(check=models.Q(('username__length__gte', 4)), name='min_username_length'),
        ),
    ]
