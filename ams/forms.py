from django.forms import ModelForm, DateInput

from ams.models import Ams


class AmsForm(ModelForm):
    class Meta:
        model = Ams
        fields = ['object_name', 'type', 'height', 'weight', 'date_birth', 'scheme',
                  'otjazhki_count', 'responsive_employee']

        widgets = {
            'date_birth': DateInput(attrs={'type': 'date'}),
        }


