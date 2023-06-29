# Generated by Django 4.1.7 on 2023-06-02 12:20

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_alter_technicheskie_usloviya_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='technicheskie_usloviya',
            name='object',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='tu', to='main.object', verbose_name='Выберите объект технических условий'),
        ),
        migrations.CreateModel(
            name='Technicheskaya_documentacia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Укажите наименование документа')),
                ('doc', models.FileField(upload_to='media/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'tiff', 'bmp', 'gif', 'pdf', 'doc', 'docx'], message='Тип файла выбран неверно.')], verbose_name='Загрузите документ')),
                ('date', models.DateField(verbose_name='Укажите дату документа')),
                ('description', models.TextField(max_length=500, verbose_name='Напишите краткое описание документа')),
                ('object', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='tehdoc', to='main.object', verbose_name='Выберите объект')),
            ],
        ),
    ]
