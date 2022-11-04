from django.db import models
from main.models import Object, Employee
from django.contrib.auth.models import User


class Ams(models.Model):
    object_name = models.ForeignKey(Object, on_delete=models.CASCADE)


class Characteristic(models.Model):
    character_instance = models.ForeignKey(Ams, on_delete=models.CASCADE)
    height = models.IntegerField()
    weight = models.IntegerField()
    type = models.CharField(max_length=30)
    date_birth = models.DateField()


class Measurments(models.Model):
    measurment_instance = models.ForeignKey(Ams, on_delete=models.CASCADE)
    year = models.DateField()
    results = models.IntegerField()
    protocol_pdf = models.FileField(upload_to='media')


class Inventory(models.Model):
    inventory_ams = models.ForeignKey(Ams, on_delete=models.CASCADE)
    inventory_number = models.IntegerField()
    inventory_name = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    mol = models.ForeignKey(Employee, on_delete=models.CASCADE)


class Diagnostic(models.Model):
    diagnostic_instance = models.ForeignKey(Ams, on_delete=models.CASCADE)
    result = models.FileField(upload_to='media')
    year = models.DateField(default=None)


class Project(models.Model):
    project_instance = models.ForeignKey(Ams, on_delete=models.CASCADE)
    documentation = models.FileField(upload_to='media')
    year = models.DateField()
    organization_name = models.CharField(max_length=50)


