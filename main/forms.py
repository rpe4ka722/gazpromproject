from django.forms import ModelForm, TextInput, Textarea, DateInput
from .models import Object, RrlLine, Position, UploadedData, Choice, Department, Technicheskie_usloviya, \
    Technicheskaya_documentacia, Scheme, Object_Foto
from django import forms


class ObjectForm(ModelForm):
    class Meta:
        model = Object
        fields = ['object_name', 'rrl_line', 'uchastok']

    uchastok = forms.ModelChoiceField(queryset=Department.objects.filter(is_prod=True),
                                      empty_label='Выберите участок связи', label='Выберите подразделение')


class RrlForm(ModelForm):
    class Meta:
        model = RrlLine
        fields = ['rrl_line_name', 'station_count', 'bandwidth']


class PositionForm(ModelForm):
    class Meta:
        model = Position
        fields = ['latitude_degrees', 'latitude_minutes', 'latitude_seconds', 'longitude_degrees', 'longitude_minutes',
                  'longitude_seconds', 'address', 'district']
        widgets = {
            'address': Textarea(attrs={'rows': '3', 'cols': '60', 'class': 'position_textarea'}),
            'district': Textarea(attrs={'rows': '3', 'cols': '60', 'class': 'position_textarea'})
        }


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


class FilterForm(forms.Form):
    ceh_list = Department.objects.filter(is_prod=True).values_list('ceh', flat=True).order_by('ceh').distinct()
    ceh = forms.ModelChoiceField(queryset=ceh_list, empty_label='все', label='Фильтровать по цеху', required=False)
    uchastok = forms.ModelChoiceField(queryset=Department.objects.filter(is_prod=True).values_list('uchastok',
                                                                                                   flat=True),
                                      empty_label='все', label='Фильтровать по участку', required=False)
    object = forms.ModelChoiceField(queryset=Object.objects.all().values_list('object_name', flat=True),
                                    empty_label='все', label='Фильтровать по объекту', required=False)



class Tu_Create_Form(ModelForm):
    class Meta:
        model = Technicheskie_usloviya
        fields = ['name', 'organization', 'proekt', 'object', 'doc', 'date', 'expire_date', 'description']

        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
            'expire_date': DateInput(attrs={'type': 'date'}),
            'description': Textarea(attrs={'rows': '3', 'cols': '60', 'class': 'position_textarea'}),
            'name': TextInput(attrs={'size': '100'}),
            'organization': TextInput(attrs={'size': '100'}),
            'proekt': TextInput(attrs={'size': '100'})
        }


class Tehdoc_Create_Form(ModelForm):
    class Meta:
        model = Technicheskaya_documentacia
        fields = ['name', 'object', 'doc', 'date', 'description']

        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
            'description': Textarea(attrs={'rows': '3', 'cols': '60', 'class': 'position_textarea'}),
            'name': TextInput(attrs={'size': '100'}),
        }


class Scheme_Create_Form(ModelForm):
    class Meta:
        model = Scheme
        fields = ['name', 'object', 'doc', 'date']

        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
            'name': TextInput(attrs={'size': '100'}),
        }


class Object_Name_Form(ModelForm):
    class Meta:
        model = Object
        fields = ['object_name']
        widgets = {
            'object_name': TextInput(attrs={'size': '50'}),
        }


class Object_Uchastok_Form(forms.Form):
    uchastok = forms.ModelChoiceField(queryset=Department.objects.filter(is_prod=True))


class Coordinat_Form(ModelForm):
    class Meta:
        model = Position
        fields = ['latitude_degrees', 'latitude_minutes', 'latitude_seconds', 'longitude_degrees', 'longitude_minutes',
                  'longitude_seconds']


class Object_Address_Form(ModelForm):
    class Meta:
        model = Position
        fields = ['address']
        widgets = {
            'address': TextInput(attrs={'size': '50'}),
        }


class Object_District_Form(ModelForm):
    class Meta:
        model = Position
        fields = ['district']
        widgets = {
            'district': TextInput(attrs={'size': '50'}),
        }


class Object_Foto_Form(ModelForm):
    class Meta:
        model = Object_Foto
        fields = ['year', 'foto']
        widgets = {
            'year': DateInput(attrs={'type': 'date'}),
            'foto_name': TextInput(attrs={'size': '50'})
        }


class List_Foto_Form(ModelForm):
    class Meta:
        model = Object_Foto
        fields = ['year', 'foto', 'object']
        widgets = {
            'year': DateInput(attrs={'type': 'date'}),
            'foto_name': TextInput(attrs={'size': '50'})
        }
