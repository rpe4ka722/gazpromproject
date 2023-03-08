from datetime import date

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.core.validators import FileExtensionValidator, MaxValueValidator, MinValueValidator
from main.models import Object
from django.shortcuts import reverse
from pathlib import Path

from rich.scripts import numeral_noun_declension


class Type(models.Model):
    name: str = models.CharField(max_length=50, verbose_name='Введите наименование оборудования')
    manufacter = models.CharField(max_length=50, blank=True, null=True, verbose_name='Укажите производителя '
                                                                                     'оборудования')
    fs_form = models.FileField(upload_to='files/', verbose_name='Загрузите форму общих технических данных',
                               validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'],
                                                                  message='Тип файла выбран неверно.')])
    frequency_range_min = models.IntegerField(verbose_name='Укажите минимальную частоту обордуования, Гц',
                                              validators=[MaxValueValidator(90000000000, message='Значение частоты не '
                                                                                                 'может быть больше 90 '
                                                                                                 'ГГц'),
                                                          MinValueValidator(0, message='Значение частоты не может быть '
                                                                                       'меньше 0')])
    frequency_range_max = models.IntegerField(verbose_name='Укажите максимальную частоту обордуования, Гц',
                                              validators=[MaxValueValidator(90000000000, message='Значение частоты не '
                                                                                                 'может быть больше '
                                                                                                 '90 ГГц'),
                                                          MinValueValidator(0, message='Значение частоты не может быть '
                                                                                       'меньше 0')])
    CLASS_CHOICES = [
        ('РРЛ', 'РРЛ'),
        ('БС конвенциональной связи', 'БС конвенциональной связи'),
        ('БС транкинговой связи', 'БС транкинговой связи'),
        ('БС', 'БС'),
        ('РЭС морской подвижной службы', 'РЭС морской подвижной службы'),
        ('РЭС сухопутной подвижной службы', 'РЭС сухопутной подвижной службы'),
        ('Судовые РЭС', 'Судовые РЭС'),
        ('АС', 'АС')]
    class_name = models.CharField(max_length=50, choices=CLASS_CHOICES, verbose_name='Выберите класс РЭС')
    frequency_str = models.CharField(max_length=50, null=True, default=None)
    # frequency_str представление в виде строки для фильтрации по диапазонам заполняется автоматически функцией
    # frequency_range

    def __str__(self):
        return self.name

    def frequency_range(self):
        # frequency_range функция поучения строки диапазона
        max_div = 0
        max_units = ''
        min_div = 0
        min_units = ''
        if 1000000 > self.frequency_range_max >= 1000:
            max_div = 1000
            max_units = 'кГц'
        elif 1000000000 > self.frequency_range_max >= 1000000:
            max_div = 1000000
            max_units = 'МГц'
        elif self.frequency_range_max >= 1000000000:
            max_div = 1000000000
            max_units = 'ГГц'
        if 1000000 > self.frequency_range_min >= 1000:
            min_div = 1000
            min_units = 'кГц'
        elif 1000000000 > self.frequency_range_min >= 1000000:
            min_div = 1000000
            min_units = 'МГц'
        elif self.frequency_range_min >= 1000000000:
            min_div = 1000000000
            min_units = 'ГГц'
        frequency_string = str(int(self.frequency_range_max/max_div)) + ' ' + max_units + ' - ' + \
                           str(int(self.frequency_range_min/min_div)) + ' ' + min_units
        self.frequency_str = frequency_string
        self.save()
        return frequency_string


class Rich(models.Model):
    name = models.CharField(max_length=30, verbose_name='Наименование', unique=True)
    start_date = models.DateField(auto_now=False, auto_now_add=False, verbose_name='Дата начала действия РИЧ')
    end_date = models.DateField(auto_now=False, auto_now_add=False, verbose_name='Дата окончания действия РИЧ')
    doc = models.FileField(upload_to='files/', validators=[FileExtensionValidator(allowed_extensions=['png', 'jpeg',
                                                                                                      'tiff', 'bmp',
                                                                                                      'gif', 'pdf',
                                                                                                      'doc', 'docx'],
                                                                                  message='Тип файла выбран неверно.')],
                           verbose_name='Копия разрешения')
    is_active = models.BooleanField()

    class Meta:
        ordering = ['-is_active', 'end_date']

    def save(self, *args, **kwargs):
        x = str(Path(self.doc.name).name.replace(Path(self.doc.name).suffix, ''))
        self.name = x.replace('_', ' ')
        if self.end_date < date.today():
            self.is_active = False
            try:
                res_obj = Res.objects.filter(related_rich=self)
                for i in res_obj:
                    i.related_rich = None
                    i.save()
            except ObjectDoesNotExist:
                pass
        else:
            self.is_active = True
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def days_left(self):
        now = date.today()
        if self.end_date < now:
            self.save()
            return 'РИЧ недействителен'
        else:
            d = self.end_date - now
            self.save()
            result = str(d.days) + ' ' + numeral_noun_declension(d.days, 'день', 'дня', 'дней')
            return result


class Registration(models.Model):
    name = models.CharField(max_length=30, verbose_name='Наименование', unique=True, null=True, blank=True)
    start_date = models.DateField(auto_now=False, auto_now_add=False, verbose_name='Укажите дату начала действия')
    end_date = models.DateField(auto_now=False, auto_now_add=False, verbose_name='Укажите дату окончания срока '
                                                                                 'действия')
    doc = models.FileField(upload_to='files/', validators=[FileExtensionValidator(allowed_extensions=['png', 'jpeg',
                                                                                                      'tiff', 'bmp',
                                                                                                      'gif', 'pdf',
                                                                                                      'doc', 'docx'],
                                                                                  message='Тип файла выбран неверно.')],
                           verbose_name='Копия свидетельства')
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        x = str(Path(self.doc.name).name.replace(Path(self.doc.name).suffix, ''))
        self.name = x.replace('_', ' ')
        if self.end_date < date.today():
            self.is_active = False
            try:
                res_obj = Res.objects.get(related_registration=self)
                res_obj.related_registration = None
                res_obj.save()
            except ObjectDoesNotExist:
                pass
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def days_left(self):
        now = date.today()
        if self.end_date < now:
            self.save()
            return 'Регистрация недействителена'
        else:
            d = self.end_date - now
            result = str(d.days) + ' ' + numeral_noun_declension(d.days, 'день', 'дня', 'дней')
            return result


class Res(models.Model):
    POLARIZATION_CHOICES = [
        ('Вертикальная', 'Вертикальная'),
        ('Горизонтальная', 'Горизонтальная'),
        ('Круговая', 'Круговая')]
    name = models.CharField(verbose_name='Наименование', max_length=20)
    related_object = models.ForeignKey(Object, on_delete=models.CASCADE, related_name='res', verbose_name='Укажите '
                                                                                                          'объект '
                                                                                                          'установки')
    related_rich = models.ForeignKey(Rich, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Выберите '
                                                                                                          'РИЧ',
                                     related_name='related_res')
    related_registration = models.OneToOneField(Registration, on_delete=models.SET_NULL, blank=True, null=True,
                                                verbose_name='Выберите регистрацию', related_name='related_res_reg')
    radio_class = models.CharField(max_length=20, blank=True, null=True, verbose_name='Введите класс излучения')
    antenna_height = models.IntegerField(blank=True,
                                         null=True,
                                         verbose_name='Укажите высоту установки антенны',
                                         validators=[
                                             MaxValueValidator(200, message='Значение высоты подвеса антенны не может '
                                                                            'быть больше 200'),
                                             MinValueValidator(0, message='Значение высоты подвеса антенны не может '
                                                                          'быть меньше 0')
                                         ]
                                         )
    azimuth_value = models.IntegerField(blank=True, null=True, verbose_name='Укажите азимут антенны',
                                        validators=[MaxValueValidator(360, message='Значение азимута не может быть '
                                                                                   'больше 360'),
                                                    MinValueValidator(0, message='Значение азимута не может быть '
                                                                                 'меньше 0')])
    antenna_gain = models.IntegerField(blank=True, null=True, verbose_name='Укажите коэффициент усиления антенны',
                                       validators=[MaxValueValidator(50, message='Значение коэффициента усиления '
                                                                                 'антенны не может быть больше 50'),
                                                   MinValueValidator(0, message='Значение коэффициента усиления антенны'
                                                                                ' не может быть меньше 0')])
    polarization = models.CharField(max_length=20, choices=POLARIZATION_CHOICES, blank=True, null=True,
                                    verbose_name='Выберите поляризацию')
    is_active = models.BooleanField(default=False)
    type = models.ForeignKey(Type, on_delete=models.SET_NULL, verbose_name='Укажите тип оборудования',
                             related_name='related_res', null=True)

    def get_absolute_url(self):
        return reverse('rich:res_detail', kwargs={'id': self.id})

    def __str__(self):
        return self.name

    def active_status(self):
        if self.related_registration and self.related_rich:
            self.related_registration.days_left()
            self.related_rich.days_left()
            if self.related_registration and self.related_rich:
                self.is_active = True
                self.save()
                return 'В работе'
        elif self.related_registration and (self.related_rich is None):
            self.related_registration = None
            self.is_active = False
            self.save()
            return 'Проектируемый'
        else:
            self.is_active = False
            self.save()
            return 'Проектируемый'


class Transmitter(models.Model):
    related_res = models.ForeignKey(Res, on_delete=models.CASCADE, related_name='transmitter')
    serial_number = models.IntegerField(blank=True, null=True)
    power = models.IntegerField(blank=True, null=True)
    transmit_frequency = models.IntegerField(blank=True, null=True)
    recieve_frequency = models.IntegerField(blank=True, null=True)


class ResProtokol(models.Model):
    TYPE_CHOICES = [
        ('измерения координат', 'измерения координат'),
        ('измерения высоты подвеса', 'измерения высоты подвеса'),
        ('измерения параметров РЭС', 'измерения параметров РЭС')]
    related_res = models.ForeignKey(Res, on_delete=models.CASCADE, related_name='protokol')
    date = models.DateField(auto_now=False, auto_now_add=False, verbose_name='Укажите дату проведения измерений')
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, verbose_name='Выберите тип протокола')
    doc = models.FileField(upload_to='files/', validators=[FileExtensionValidator(allowed_extensions=['png', 'jpeg',
                                                                                                      'tiff', 'bmp',
                                                                                                      'gif', 'pdf',
                                                                                                      'doc', 'docx'],
                                                                                  message='Тип файла выбран неверно.')],
                           verbose_name='Загрузите протокол')
    name = models.CharField(max_length=30, null=True)

    def save(self, *args, **kwargs):
        self.name = 'Протокол ' + self.type + ' от ' + str(self.date.year) + ' года'
        super().save(*args, **kwargs)
