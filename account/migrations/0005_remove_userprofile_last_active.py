# Generated by Django 4.1.7 on 2023-03-12 13:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_userprofile_last_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='last_active',
        ),
    ]
