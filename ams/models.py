from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.db import models
from django.urls import reverse

from main.models import Object
from django.contrib.auth.models import User


class Inventory(models.Model):
    inventory_number = models.IntegerField(null=True, blank=True, verbose_name='Укажите инвентарный номер')
    inventory_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='Укажите наименование объекта')
    description = models.TextField(max_length=1000, null=True, blank=True, verbose_name='Укажите краткую характеристику '
                                                                                       'объекта')
    owner = models.CharField(max_length=50, verbose_name='Укажите организацию')

    def __str__(self):
        return self.inventory_name


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
    object_name = models.OneToOneField(Object, on_delete=models.CASCADE, verbose_name='Выберите объект',
                                    related_name='ams')
    height = models.IntegerField(verbose_name='Укажите высоту АМС, м', null=True, blank=True,
                                 validators=[MinValueValidator(0, message='Значение не может быть отрицательным'),
                                             MaxValueValidator(250, message='Значение не может быть больше 250')])
    weight = models.IntegerField(verbose_name='Укажите вес АМС, т', null=True, blank=True,
                                 validators=[MinValueValidator(0, message='Значение не может быть отрицательным'),
                                             MaxValueValidator(1000, message='Значение не может быть больше 1000')])
    type = models.CharField(verbose_name='Выберите тип АМС', max_length=30, choices=TYPE_CHOICES, null=True)
    date_birth = models.DateField(verbose_name='Укажите дату ввода АМС в эксплуатацию', null=True, blank=True)
    scheme = models.FileField(upload_to='files/', validators=[FileExtensionValidator(allowed_extensions=['png', 'jpeg',
                                                                                                         'tiff', 'bmp',
                                                                                                         'gif', 'pdf',
                                                                                                         'vsd', 'vsdx'],
                                                                                     message='Тип файла выбран неверно.'
                                                                                             )],
                              verbose_name='Выберите схему АМС', null=True, blank=True)
    is_dangerous = models.BooleanField(default=False)
    otjazhki = models.BooleanField(default=False)
    otjazhki_count = models.IntegerField(choices=COUNT_CHOICES, default=0, verbose_name='Укажите количество ярусов '
                                                                                        'оттяжек')
    responsive_employee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                            verbose_name='Выберите ответственного за эксплуатацию', blank=True)
    passport = models.FileField(upload_to='media', verbose_name='Загрузите паспорт АМС', null=True, blank=True,
                                validators=[FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'tiff', 'bmp',
                                                                                       'docx', 'pdf', 'doc', 'vsdx'],
                                                                   message='Тип файла выбран неверно.')])
    inventory = models.ForeignKey(Inventory, on_delete=models.DO_NOTHING, related_name='ams', null=True)

    def save(self, *args, **kwargs):
        if self.height >= 100:
            self.is_dangerous = True
        if self.otjazhki_count != 0:
            self.otjazhki = True
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('ams:ams_detail', kwargs={'ams_id': self.id})

    def get_last_otklonenie(self):
        protocol_list = Measurments.objects.filter(measurment_instance=self)
        if protocol_list:
            last_protocol = None
            for item in protocol_list:
                if last_protocol is None or last_protocol.year < item.year:
                    last_protocol = item
                item.is_last = False
                item.save()
            last_protocol.is_last = True
            last_protocol.save()
            return last_protocol
        else:
            return '-'


class Measurments(models.Model):
    measurment_instance = models.ForeignKey(Ams, on_delete=models.CASCADE, related_name='protocol')
    year = models.DateField(verbose_name='Укажите дату проведения измерений')
    results = models.IntegerField(verbose_name='Укажите максимальное отклонение в мм',
                                  validators=[MinValueValidator(0, message='Значение не может быть отрицательным'),
                                              MaxValueValidator(10000, message='Значение не может быть больше 10000')])
    protocol_pdf = models.FileField(upload_to='media', validators=[FileExtensionValidator(allowed_extensions=['png',
                                                                                                              'jpeg',
                                                                                                              'tiff',
                                                                                                              'bmp',
                                                                                                              'doc',
                                                                                                              'pdf',
                                                                                                              'jpg',
                                                                                                              'docx'],
                                                                                          message='Тип файла выбран '
                                                                                                  'неверно.')],
                                    verbose_name='Загрузите протокол измерений')
    is_otklonenie = models.BooleanField(default=False)
    is_last = models.BooleanField(default=False)

    class Meta:
        ordering = ['year']

    def save(self, *args, **kwargs):
        max_value = self.measurment_instance.height
        if int(self.results) > max_value:
            self.is_otklonenie = True
        else:
            self.is_otklonenie = False
        super().save(*args, **kwargs)

    def otklonenie(self):
        return self.results - self.measurment_instance.height


class Diagnostic(models.Model):
    diagnostic_instance = models.ForeignKey(Ams, on_delete=models.CASCADE, related_name='diagnostic')
    result = models.FileField(upload_to='media', validators=[FileExtensionValidator(allowed_extensions=['png', 'jpeg',
                                                                                                        'tiff', 'bmp',
                                                                                                        'gif', 'pdf',
                                                                                                        'jpg'],
                                                                                    message='Тип файла выбран '
                                                                                            'неверно.')],
                              verbose_name='Загрузите результаты диагностического обследования')
    year = models.DateField(default=None, verbose_name='Укажите дату проведения обследования')


class Project(models.Model):
    project_instance = models.ForeignKey(Ams, on_delete=models.CASCADE, related_name='project')
    documentation = models.FileField(upload_to='media', validators=[FileExtensionValidator(allowed_extensions=['png',
                                                                                                               'jpeg',
                                                                                                               'tiff',
                                                                                                               'bmp',
                                                                                                               'gif',
                                                                                                               'pdf',
                                                                                                               'jpg'],
                                                                                           message='Тип файла выбран '
                                                                                                   'неверно.')],
                                     verbose_name='Загрузите результаты диагностического обследования')
    year = models.DateField(verbose_name='Укажите дату разработки документации')
    organization_name = models.CharField(max_length=50, verbose_name='Укажите наименование проектного института')


class Sez(models.Model):
    sez_instance = models.ForeignKey(Ams, on_delete=models.CASCADE, related_name='sez')
    sez_protocol = models.FileField(upload_to='media', validators=[FileExtensionValidator(allowed_extensions=['png',
                                                                                                               'jpeg',
                                                                                                               'tiff',
                                                                                                               'bmp',
                                                                                                               'doc',
                                                                                                              'docx',
                                                                                                               'pdf',
                                                                                                               'jpg'],
                                                                                          message='Тип файла выбран '
                                                                                                  'неверно.')],
                                    verbose_name='Загрузите санитарно-экологическое заключение')
    year = models.DateField(default=None, verbose_name='Укажите дату разработки документации')


class Foto_Ams(models.Model):
    foto_instance = models.ForeignKey(Ams, on_delete=models.CASCADE, related_name='foto')
    foto_name = models.CharField(max_length=50)
    foto = models.ImageField(upload_to='media', validators=[FileExtensionValidator(message='Тип файла выбран неверно.',
                                                                                   allowed_extensions=['png', 'jpeg',
                                                                                                       'tiff', 'bmp',
                                                                                                       'gif', 'jpg'])],
                             verbose_name='Выберите фотографию АМС')
    year = models.DateField(default=None, verbose_name='Укажите ориентировочную дату фото')



