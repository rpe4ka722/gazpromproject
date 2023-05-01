from django.forms import ModelForm, DateInput
from django import forms

from ams.models import Ams, Foto_Ams, Measurments, Diagnostic, Project, Sez, Inventory


class AmsForm(ModelForm):
    class Meta:
        model = Ams
        fields = ['object_name', 'type', 'height', 'weight', 'date_birth', 'scheme',
                  'otjazhki_count', 'responsive_employee']

        widgets = {
            'date_birth': DateInput(attrs={'type': 'date'}),
        }


class AmsTypeForm(ModelForm):
    class Meta:
        model = Ams
        fields = ['type']


class SchemeForm(ModelForm):
    class Meta:
        model = Ams
        fields = ['scheme']


class FotoAmsForm(ModelForm):
    class Meta:
        model = Foto_Ams
        fields = ['year', 'foto']
        widgets = {
            'year': DateInput(attrs={'type': 'date'})
        }


class ProtocolForm(ModelForm):
    class Meta:
        model = Measurments
        fields = ['protocol_pdf', 'year', 'results']
        widgets = {
            'year': DateInput(attrs={'type': 'date'})
        }


class DiagnosticForm(ModelForm):
    class Meta:
        model = Diagnostic
        fields = ['result', 'year']
        widgets = {
            'year': DateInput(attrs={'type': 'date'})
        }


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['organization_name', 'documentation', 'year']
        widgets = {
            'year': DateInput(attrs={'type': 'date'})
        }


class SezForm(ModelForm):
    class Meta:
        model = Sez
        fields = ['sez_protocol', 'year']
        widgets = {
            'year': DateInput(attrs={'type': 'date'})
        }


class InventoryForm(ModelForm):
    class Meta:
        model = Inventory
        fields = ['inventory_number', 'inventory_name', 'description', 'owner']


class PassportForm(ModelForm):
    class Meta:
        model = Ams
        fields = ['passport']

