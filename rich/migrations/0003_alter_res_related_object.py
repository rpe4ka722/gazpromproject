# Generated by Django 4.0.3 on 2023-01-04 13:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_alter_podano_na_vipolnenie_otklonit_comment'),
        ('rich', '0002_res_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='res',
            name='related_object',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='res', to='main.object'),
        ),
    ]
