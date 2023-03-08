import re

from django.forms import ModelForm, DateInput
from django import forms
from rich.models import Type, Rich, Registration, Res, Transmitter, ResProtokol
from main.models import Object


class RichForm(ModelForm):
    class Meta:
        model = Rich
        fields = ['start_date', 'end_date', 'doc']
        widgets = {
            'start_date': DateInput(attrs={'type': 'date'}),
            'end_date': DateInput(attrs={'type': 'date'}),
        }


class RegistrationForm(ModelForm):
    class Meta:
        model = Registration
        fields = ['start_date', 'end_date', 'doc']
        widgets = {
            'start_date': DateInput(attrs={'type': 'date'}),
            'end_date': DateInput(attrs={'type': 'date'}),
        }


class ResForm(ModelForm):
    class Meta:
        model = Res
        fields = ['name', 'related_object', 'related_rich', 'related_registration', 'radio_class', 'antenna_height',
                  'azimuth_value', 'antenna_gain', 'polarization', 'type']

    def clean_name(self):
        data = self.cleaned_data['name']
        if data and not re.match(r'^[a-zA-Zа-яА-Я0-9]+$', data):
            raise forms.ValidationError('В имени недопустимые символы!')
        return data


class ResNameForm(ModelForm):
    class Meta:
        model = Res
        fields = ['name']

    def clean_name(self):
        data = self.cleaned_data['name']
        if data and not re.match(r'^[a-zA-Zа-яА-Я0-9]+$', data):
            raise forms.ValidationError('Недопустимые символы!')
        return data


class ResClassForm(ModelForm):
    class Meta:
        model = Res
        fields = ['radio_class']

    def clean_radio_class(self):
        data = self.cleaned_data['radio_class']
        if data and not re.match(r'^[a-zA-Zа-яА-Я0-9]+$', data):
            raise forms.ValidationError('Недопустимые символы!')
        return data


class TransmitterForm(ModelForm):
    class Meta:
        model = Transmitter
        fields = ['related_res', 'serial_number', 'power', 'transmit_frequency', 'recieve_frequency']


class RegForm(RegistrationForm, forms.Form):
    related_object = forms.ModelChoiceField(queryset=Object.objects.all(), empty_label='', label='Выберите объект')
    related_res = forms.ModelChoiceField(queryset=Res.objects.all(), empty_label='', label='Выберите РЭС для '
                                                                                           'регистрации')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['related_res'].queryset = Res.objects.none()

        if 'related_object' in self.data:
            try:
                object_id = int(self.data.get('related_object'))
                self.fields['related_res'].queryset = Res.objects.filter(related_object=object_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty queryset


class TypeForm(ModelForm):
    class Meta:
        model = Type
        fields = ['name', 'manufacter', 'fs_form', 'frequency_range_min', 'frequency_range_max', 'class_name']


class ResProtokolForm(ModelForm):
    class Meta:
        model = ResProtokol
        fields = ['type', 'date', 'doc']
        widgets = {
            'date': DateInput(attrs={'type': 'date'})
        }

