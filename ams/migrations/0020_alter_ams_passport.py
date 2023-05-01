# Generated by Django 4.1.7 on 2023-04-23 19:47

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ams', '0019_alter_inventory_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ams',
            name='passport',
            field=models.FileField(blank=True, null=True, upload_to='media', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'tiff', 'bmp', 'gif', 'pdf', 'vsd', 'vsdx'], message='Тип файла выбран неверно.')], verbose_name='Загрузите паспорт АМС'),
        ),
    ]
