from django import forms 
from patients.models import Patient

class PatientForm(forms.ModelForm):
    


	class Meta:
		model = Patient
		fields = '__all__'

def form_validation_error(form):
    msg = ""
    for field in form:
        for error in field.errors:
            msg += "%s: %s \\n" % (field.label if hasattr(field, 'label') else 'Error', error)
    return msg
