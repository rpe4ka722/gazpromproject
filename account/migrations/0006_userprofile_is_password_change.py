# Generated by Django 4.1.7 on 2023-03-19 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_remove_userprofile_last_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_password_change',
            field=models.BooleanField(default=False),
        ),
    ]