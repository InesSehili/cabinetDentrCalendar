from django import forms 
from ordonances.models import Ordonance



class OrdonanceForm (forms.ModelForm):


	class Meta:
		model = Ordonance
		fields = '__all__'


def form_validation_error(form):
	msg= ""
	for field in form:
		for error in field.errors:
			msg += "%s: %s \\n" % (field.label if hasattr(field, 'label') else 'Error', error)
			return msg