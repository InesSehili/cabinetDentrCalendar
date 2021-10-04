from django import forms 
from rdvs.models import Rdv

class RdvForm(forms.ModelForm):
    date_rdv= forms.DateTimeField(
      input_formats = ['%Y-%m-%dT%H:%M'],
          widget = forms.DateTimeInput(
            attrs={
            'type': 'datetime-local',
            'class': 'form-control'},
        format='%Y-%m-%dT%H:%M'))
    date_fin= forms.DateTimeField(
      input_formats = ['%Y-%m-%dT%H:%M'],
          widget = forms.DateTimeInput(
            attrs={
            'type': 'datetime-local',
            'class': 'form-control'},
        format='%Y-%m-%dT%H:%M'))
    class Meta:
        model = Rdv
        fields = '__all__'
def form_validation_error(form):
    msg = ""
    for field in form:
        for error in field.errors:
            msg += "%s: %s \\n" % (field.label if hasattr(field, 'label') else 'Error', error)
    return msg









