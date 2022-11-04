from django.forms import ModelForm
from .models import Object, RrlLine, Position, UploadedData, Choice, Department, Employee, Ozp


class ObjectForm(ModelForm):
    class Meta:
        model = Object
        fields = ['object_name', 'rrl_line', 'uchastok']


class RrlForm(ModelForm):
    class Meta:
        model = RrlLine
        fields = ['rrl_line_name', 'station_count', 'bandwidth']


class PositionForm(ModelForm):
    class Meta:
        model = Position
        fields = ['latitude_degrees', 'latitude_minutes', 'latitude_seconds', 'longitude_degrees', 'longitude_minutes',
                  'longitude_seconds', 'address', 'district']


class UploadXlsForm(ModelForm):
    class Meta:
        model = UploadedData
        fields = ['file']


class UploadChoiceForm(ModelForm):
    class Meta:
        model = Choice
        fields = ['sheet', 'row']


class ImportForm(ModelForm):
    class Meta:
        model = Choice
        fields = ['object_name', 'coords_lat', 'coords_lon', 'district', 'address']


class DepartmentForm(ModelForm):
    class Meta:
        model = Department
        fields = ['ceh', 'uchastok']


class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = ['employee_name', 'employee_last_name']




