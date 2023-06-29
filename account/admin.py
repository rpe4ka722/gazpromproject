from django.contrib import admin
from main.models import Department
from account.models import Userprofile

admin.site.register(Department)
admin.site.register(Userprofile)