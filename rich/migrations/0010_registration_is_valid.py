# Generated by Django 4.1.7 on 2023-02-26 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rich', '0009_alter_res_related_registration_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='is_valid',
            field=models.BooleanField(default=True),
        ),
    ]