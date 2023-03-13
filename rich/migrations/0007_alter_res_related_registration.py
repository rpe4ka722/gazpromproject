# Generated by Django 4.0.3 on 2023-02-19 17:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rich', '0006_alter_rich_options_alter_res_related_registration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='res',
            name='related_registration',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='related_res_reg', to='rich.registration', verbose_name='Выберите регистрацию'),
        ),
    ]
