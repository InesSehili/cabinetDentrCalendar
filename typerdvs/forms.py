from django import forms 
from typerdvs.models import Typerdv


class TyperdvForm(forms.ModelForm):



	class Meta:
		model = Typerdv
		fields = '__all__'

def form_validation_error(form):
	msg = ""
	for field in form:
		for error in field.errors:
			msg += "%s: %s \\n" % (field.label if hasattr(field, 'label') else 'Error', error)
			return msg
