from django.forms import ModelForm
from models import Class, Type, Rich, Registration, Res, Transmitter


class ClassForm(ModelForm):
    class Meta:
        model = Class
        fields = ['name']


class TypeForm(ModelForm):
    class Meta:
        model = Type
        fields = ['name', 'manufacter', 'fs_form', 'class_res', 'frequency_range_min', 'frequency_range_max']


class RichForm(ModelForm):
    class Meta:
        model = Rich
        fields = ['name', 'start_date', 'end_date', 'doc']


class RegistrationForm(ModelForm):
    class Meta:
        model = Registration
        fields = ['start_date', 'end_date', 'doc']


class ResForm(ModelForm):
    class Meta:
        model = Res
        fields = ['start_date', 'related_object', 'related_rich', 'related_registration', 'radio_class',
                  'antenna_height', 'azimuth_value', 'antenna_gain', 'polarization', 'is_active']