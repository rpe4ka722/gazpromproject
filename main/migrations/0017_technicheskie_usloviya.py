# Generated by Django 4.1.7 on 2023-05-28 12:36

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_alter_ozp_object_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Technicheskie_usloviya',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('organization', models.CharField(max_length=100)),
                ('proekt', models.CharField(max_length=150)),
                ('doc', models.FileField(upload_to='media/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'tiff', 'bmp', 'gif', 'pdf', 'doc', 'docx'], message='Тип файла выбран неверно.')])),
                ('date', models.DateField()),
                ('description', models.TextField(max_length=500)),
                ('expire_date', models.DateField(default=datetime.datetime(2025, 5, 27, 12, 36, 49, 76323))),
                ('object', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main.object')),
            ],
        ),
    ]
