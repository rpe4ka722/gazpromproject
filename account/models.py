from django.db import models
from django.contrib.auth.models import User

from main.models import Department


class Userprofile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='profile')
    department = models.ForeignKey(Department, null=True, on_delete=models.DO_NOTHING)

