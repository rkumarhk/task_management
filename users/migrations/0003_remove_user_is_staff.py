# Generated by Django 5.2 on 2025-04-25 07:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_rename_role_user_job_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_staff',
        ),
    ]
