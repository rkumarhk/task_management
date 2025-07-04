# Generated by Django 5.2 on 2025-04-23 16:59

import django.contrib.auth.validators
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(blank=True, max_length=255, null=True)),
                ('middle_name', models.CharField(blank=True, max_length=255, null=True)),
                ('country_code', models.CharField(blank=True, max_length=4, null=True)),
                ('phone', models.CharField(blank=True, max_length=10, null=True)),
                ('is_phone_verified', models.BooleanField(default=False)),
                ('is_email_verified', models.BooleanField(default=False)),
                ('otp', models.CharField(blank=True, max_length=6, null=True)),
                ('otp_created_at', models.DateTimeField(blank=True, null=True)),
                ('state', models.CharField(blank=True, max_length=2, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('country_name', models.CharField(blank=True, max_length=100, null=True)),
                ('zip_code', models.CharField(blank=True, max_length=10, null=True)),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='profile_pics/')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('role', models.CharField(choices=[('superadmin', 'SuperAdmin'), ('admin', 'Admin'), ('projectmanager', 'Project Manager'), ('projectlead', 'Project Lead'), ('developer', 'Developer'), ('client', 'Client')], default='developer', max_length=16)),
                ('account_status', models.CharField(blank=True, choices=[('pending', 'Pending'), ('suspended', 'Suspended'), ('active', 'Active')], max_length=10, null=True)),
                ('fcm', models.CharField(blank=True, max_length=510, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to.', related_name='custom_user_set', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='custom_user_set', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'ordering': ('id',),
            },
        ),
    ]
