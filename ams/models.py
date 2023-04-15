from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.shortcuts import redirect
from django.urls import reverse

from main.models import Object
from django.contrib.auth.models import User


class Ams(models.Model):
    TYPE_CHOICES = [
        ('Башня', 'Башня'),
        ('Мачта', 'Мачта'),
        ('Трубостойка', 'Трубостойка')
    ]
    COUNT_CHOICES = [
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    ]
    object_name = models.ForeignKey(Object, on_delete=models.CASCADE, verbose_name='Выберите объект')
    height = models.IntegerField(verbose_name='Укажите высоту АМС, м', null=True, blank=True,
                                 validators=[MinValueValidator(0, message='Значение не может быть отрицательным'),
                                             MaxValueValidator(250, message='Значение не может быть больше 250')])
    weight = models.IntegerField(verbose_name='Укажите вес АМС, т', null=True, blank=True,
                                 validators=[MinValueValidator(0, message='Значение не может быть отрицательным'),
                                             MaxValueValidator(250, message='Значение не может быть больше 250')])
    type = models.CharField(verbose_name='Выберите тип АМС', max_length=30, choices=TYPE_CHOICES, null=True)
    date_birth = models.DateField(verbose_name='Укажите дату ввода АМС в эксплуатацию', null=True, blank=True)
    scheme = models.FileField(upload_to='media', verbose_name='Схема АМС', null=True, blank=True)
    is_dangerous = models.BooleanField(default=False)
    otjazhki = models.BooleanField(default=False)
    otjazhki_count = models.IntegerField(choices=COUNT_CHOICES, default=0, verbose_name='Укажите количество оттяжек')
    responsive_employee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                            verbose_name='Выберите ответственного за эксплуатацию', blank=True)
    passport = models.FileField(upload_to='media', verbose_name='Паспорт АМС', null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.height <= 100:
            self.is_dangerous = True
        elif self.otjazhki_count != 0:
            self.otjazhki = True
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('ams:ams_detail', kwargs={'ams_id': self.id})


class Measurments(models.Model):
    measurment_instance = models.ForeignKey(Ams, on_delete=models.CASCADE, related_name='protocol')
    year = models.DateField()
    results = models.IntegerField()
    protocol_pdf = models.FileField(upload_to='media')


class Inventory(models.Model):
    inventory_ams = models.ForeignKey(Ams, on_delete=models.CASCADE, related_name='inventory')
    inventory_number = models.IntegerField()
    inventory_name = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    owner = models.CharField(max_length=50)


class Diagnostic(models.Model):
    diagnostic_instance = models.ForeignKey(Ams, on_delete=models.CASCADE, related_name='diagnostic')
    result = models.FileField(upload_to='media')
    year = models.DateField(default=None)


class Project(models.Model):
    project_instance = models.ForeignKey(Ams, on_delete=models.CASCADE, related_name='project')
    documentation = models.FileField(upload_to='media')
    year = models.DateField()
    organization_name = models.CharField(max_length=50)


class Sez(models.Model):
    sez_instance = models.ForeignKey(Ams, on_delete=models.CASCADE, related_name='sez')
    sez_protocol = models.FileField(upload_to='media')
    year = models.DateField(default=None)


class Foto_Ams(models.Model):
    foto_instance = models.ForeignKey(Ams, on_delete=models.CASCADE, related_name='foto')
    foto_name = models.CharField(max_length=50)
    foto = models.ImageField(upload_to='media')
    year = models.DateField(default=None)



