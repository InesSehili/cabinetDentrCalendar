from django.shortcuts import render
from typerdvs.forms import TyperdvForm, form_validation_error
from typerdvs.models import Typerdv
from django.contrib import messages

# Create your views here.
def formulaire_ajout_type_rdv(request):
	context = {}
	context['typrrdv_list'] = Typerdv.objects.all()
	return render (request , "ajouter-type-rdvs.html", context)


def ajouter_type_rdv(request):

	context = {}
	if request.method == "POST":
		form = TyperdvForm(request.POST or None)
		if form.is_valid():
		 	print("form is valid")
		 	form.save()
		 	messages.success(request, 'type de rendez-vous a été bien crée')
		 	context['typrrdv_list'] = Typerdv.objects.all()
		 	return render (request , "ajouter-type-rdvs.html", context)
		else:
		 	messages.error(request, form_validation_error(form))
		 	context['typrrdv_list'] = Typerdv.objects.all()
		 	return render (request , "ajouter-type-rdvs.html", context)

	return render(request, 'ajouter-type-rdvs.html', {})



def supprimer_type_rdv(request):
	context = {}
	if request.method == "POST":
		id_type = request.POST.get("id")
		print("id type" + id_type)

	Typerdv.objects.get(id=id_type).delete()
	context['typrrdv_list'] = Typerdv.objects.all()
	return render (request , "ajouter-type-rdvs.html", context)






            


