# Generated by Django 4.0.3 on 2022-11-25 12:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_alter_podano_na_vipolnenie_zamechanie'),
    ]

    operations = [
        migrations.AddField(
            model_name='podano_na_vipolnenie',
            name='otklonit_comment',
            field=models.TextField(default=1, max_length=500),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='podano_na_vipolnenie',
            name='zamechanie',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='podano_na_vipolnenie', to='main.ozp'),
        ),
    ]