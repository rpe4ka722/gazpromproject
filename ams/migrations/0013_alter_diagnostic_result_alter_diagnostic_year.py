# Generated by Django 4.1.7 on 2023-04-23 08:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ams', '0012_measurments_is_otklonenie_alter_foto_ams_foto_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diagnostic',
            name='result',
            field=models.FileField(upload_to='media', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'tiff', 'bmp', 'gif', 'pdf', 'jpg'], message='Тип файла выбран неверно.')], verbose_name='Загрузите результаты диагностического обследования'),
        ),
        migrations.AlterField(
            model_name='diagnostic',
            name='year',
            field=models.DateField(default=None, verbose_name='Укажите дату проведения обследования'),
        ),
    ]
