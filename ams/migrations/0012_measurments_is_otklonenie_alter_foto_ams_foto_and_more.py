# Generated by Django 4.1.7 on 2023-04-16 20:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ams', '0011_alter_ams_otjazhki_count_alter_ams_scheme_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='measurments',
            name='is_otklonenie',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='foto_ams',
            name='foto',
            field=models.ImageField(upload_to='media', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'tiff', 'bmp', 'gif', 'jpg'], message='Тип файла выбран неверно.')], verbose_name='Выберите фотографию АМС'),
        ),
        migrations.AlterField(
            model_name='foto_ams',
            name='year',
            field=models.DateField(default=None, verbose_name='Укажите ориентировочную дату фото'),
        ),
        migrations.AlterField(
            model_name='measurments',
            name='protocol_pdf',
            field=models.FileField(upload_to='media', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'tiff', 'bmp', 'gif', 'pdf', 'jpg'], message='Тип файла выбран неверно.')], verbose_name='Загрузите протокол измерений'),
        ),
        migrations.AlterField(
            model_name='measurments',
            name='results',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0, message='Значение не может быть отрицательным'), django.core.validators.MaxValueValidator(10000, message='Значение не может быть больше 10000')], verbose_name='Укажите максимальное отклонение в мм'),
        ),
        migrations.AlterField(
            model_name='measurments',
            name='year',
            field=models.DateField(verbose_name='Укажите дату проведения измерений'),
        ),
    ]
