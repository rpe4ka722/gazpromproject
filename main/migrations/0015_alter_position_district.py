# Generated by Django 4.1.7 on 2023-05-26 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_department_is_prod'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='district',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='район'),
        ),
    ]
