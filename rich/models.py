from django.db import models
from django.core.validators import FileExtensionValidator
from main.models import Object


class Class(models.Model):
    CLASS_CHOICES = [
        ('РРЛ', 'РРЛ'),
        ('БС конвенциональной связи', 'БС конвенциональной связи'),
        ('БС транкинговой связи', 'БС транкинговой связи'),
        ('БС', 'БС'),
        ('РЭС морской подвижной службы', 'РЭС морской подвижной службы'),
        ('РЭС сухопутной подвижной службы', 'РЭС сухопутной подвижной службы'),
        ('Судовые РЭС', 'Судовые РЭС'),
        ('АС', 'АС')]
    name = models.CharField(max_length=50, choices=CLASS_CHOICES, verbose_name='класс РЭС')


class Type(models.Model):
    name = models.CharField(max_length=50)
    manufacter = models.CharField(max_length=50, blank=True, null=True)
    fs_form = models.FileField(upload_to='files/', validators=[FileExtensionValidator(allowed_extensions=
                                                                                      ['.png', '.jpeg', '.tiff', '.bmp',
                                                                                       '.gif', '.pdf', '.doc', '.docx'],
                                                                                      message='Тип файла выбран '
                                                                                              'неверно.')])
    class_res = models.ForeignKey(Class, on_delete=models.DO_NOTHING, related_name='class_res')
    frequency_range_min = models.FloatField()
    frequency_range_max = models.FloatField()


class Rich(models.Model):
    name = models.CharField(max_length=30)
    start_date = models.DateField(auto_now=False, auto_now_add=False)
    end_date = models.DateField(auto_now=False, auto_now_add=False)
    doc = models.FileField(upload_to='files/', validators=[FileExtensionValidator(allowed_extensions=['.png', '.jpeg',
                                                                                                      '.tiff', '.bmp',
                                                                                                      '.gif', '.pdf',
                                                                                                      '.doc', '.docx'],
                                                                                  message='Тип файла выбран неверно.')])


class Registration(models.Model):
    start_date = models.DateField(auto_now=False, auto_now_add=False)
    end_date = models.DateField(auto_now=False, auto_now_add=False)
    doc = models.FileField(upload_to='files/', validators=[FileExtensionValidator(allowed_extensions=['.png', '.jpeg',
                                                                                                      '.tiff', '.bmp',
                                                                                                      '.gif', '.pdf',
                                                                                                      '.doc', '.docx'],
                                                                                  message='Тип файла выбран неверно.')])


class Res(models.Model):
    POLARIZATION_CHOICES = [
        ('Вертикальная', 'Вертикальная'),
        ('Горизонтальная', 'Горизонтальная'),
        ('Круговая', 'Круговая')]
    name = models.CharField(max_length=20)
    related_object = models.ForeignKey(Object, on_delete=models.CASCADE, related_name='res')
    related_rich = models.ForeignKey(Rich, on_delete=models.DO_NOTHING, blank=True, null=True)
    related_registration = models.ForeignKey(Registration, on_delete=models.DO_NOTHING, blank=True, null=True)
    radio_class = models.CharField(max_length=20, blank=True, null=True)
    antenna_height = models.IntegerField(blank=True, null=True)
    azimuth_value = models.IntegerField(blank=True, null=True)
    antenna_gain = models.IntegerField(blank=True, null=True)
    polarization = models.CharField(max_length=20, choices=POLARIZATION_CHOICES, blank=True, null=True)
    is_active = models.BooleanField(default=False)


class Transmitter(models.Model):
    related_res = models.ForeignKey(Res, on_delete=models.CASCADE, related_name='transmitter')
    serial_number = models.IntegerField(blank=True, null=True)
    power = models.IntegerField(blank=True, null=True)
    transmit_frequency = models.IntegerField(blank=True, null=True)
    recieve_frequency = models.IntegerField(blank=True, null=True)



