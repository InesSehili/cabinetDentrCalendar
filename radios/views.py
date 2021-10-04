from django.shortcuts import render,  redirect
from radios.forms import RadioForm, form_validation_error
from patients.models import Patient
from django.contrib import messages
from radios.models import Radio
import decimal
from django.contrib.auth.decorators import login_required
from core.decorators import allowed_users

# Create your views here.
@login_required(login_url="/login/")
@allowed_users(allowed_roles=['dentiste'])
def ajouter_radio(request):
	context = {}
	if request.method == 'POST':
		
		id_patient = request.POST.get('patient')
		prix_radio = request.POST.get('prix_radio')
		
		print("id_patient: "+id_patient)
		nom = Patient.objects.get(id=id_patient).nom
		prenom = Patient.objects.get(id=id_patient).prenom
		form = RadioForm(request.POST, request.FILES)
		if form.is_valid():
			print("form is valid")
			radio = form.save()
			last_radio = Radio.objects.last().id
			Radio.objects.filter(id=last_radio).update(reste=prix_radio)




			Patient.objects.filter(id=id_patient).update(radio_existe=True)
			prix_total_patient = Patient.objects.get(id=id_patient).total_payement
			reste_paye_patient = Patient.objects.get(id=id_patient).reste_paye
			prix_paye_patient = Patient.objects.get(id=id_patient).prix_paye
			Patient.objects.filter(id=id_patient).update(total_payement=prix_total_patient+decimal.Decimal(prix_radio))
			prix_total_patient_2 = Patient.objects.get(id=id_patient).total_payement
			Patient.objects.filter(id=id_patient).update(reste_paye=prix_total_patient_2- prix_paye_patient)
			messages.success(request, 'Radio crée')
			context['radio_liste'] = Radio.objects.filter(patient=id_patient)
			context['id'] = id_patient
			context['nom'] = nom
			context['prenom'] = prenom
			return render(request, "liste-radio-patient.html", context)
			
		else:
			messages.error(request, "Prix radio erroné")
	context['patient_list'] = Patient.objects.filter(archiver=False).values().order_by('updated_at')
	return render(request, "liste-patient.html", context)

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['dentiste'])
def formulaire_ajout_radio(request):
	context = {}
	if request.method =='POST':
		nom_patient = request.POST.get('nom')
		prenom_patient = request.POST.get('prenom')
		id_patient = request.POST.get('patient')
		print("id_patient: "+id_patient)
		print("nom = ", nom_patient)
		print("prenom = ", prenom_patient)
		
	context['nom_patient'] = nom_patient
	context['prenom_patient'] = prenom_patient
	context['id_patient'] = id_patient

	return render(request, "ajouter-radio.html", context)
@login_required(login_url="/login/")
@allowed_users(allowed_roles=['dentiste'])
def liste_radio(request):
	context = {}
	context['segment'] = 'radios'
	context['radio_liste'] = Radio.objects.all().order_by('updated_at')
	return render(request, "liste-radio.html", context)
@login_required(login_url="/login/")
@allowed_users(allowed_roles=['dentiste'])
def supprimer_radio(request):
	context = {}
	if request.method =="POST":
		id_radio = request.POST.get('id-radio')
		id_patient = request.POST.get('id-patient')
	radio=Radio.objects.get(id=id_radio)
	prix_radio = radio.prix_radio
	prix_paye = radio.prix_paye
	if prix_paye >0:
		messages.error(request, "vous pouvez pas supprimer cet element car il est deja payé")
		context['radio_liste'] = Radio.objects.all().order_by('updated_at')
		return render(request, "liste-radio.html", context)


	else:
		radio.delete()
		prix_total_patient = Patient.objects.get(id=id_patient).total_payement
		reste_paye_patient = Patient.objects.get(id=id_patient).reste_paye
		prix_paye_patient = Patient.objects.get(id=id_patient).prix_paye
		Patient.objects.filter(id=id_patient).update(total_payement=prix_total_patient-decimal.Decimal(prix_radio))
		prix_total_patient_2 = Patient.objects.get(id=id_patient).total_payement
		Patient.objects.filter(id=id_patient).update(reste_paye=prix_total_patient_2- prix_paye_patient)

		radios = Radio.objects.filter(patient=id_patient)
		print("query is ",  not radios.exists())
		if not radios.exists():
			Patient.objects.filter(id=id_patient).update(radio_existe=False)

		
		context['radio_liste'] = Radio.objects.all().order_by('updated_at')
		return render(request, "liste-radio.html", context)

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['dentiste'])
def afficher_radio(request):
	context = {}
	if request.method =='POST':
		id_radio = request.POST.get('id_radio')
		nom_patient = request.POST.get('nom')
		print("nom"+nom_patient)

		prenom_patient = request.POST.get('prenom')
		print("prenom"+prenom_patient)
	radio = Radio.objects.get(id=id_radio)
	context['radio'] = radio
	context['nom_patient'] = nom_patient
	context['prenom_patient'] = prenom_patient



	return render(request, "afficher-radio.html", context)
@login_required(login_url="/login/")
@allowed_users(allowed_roles=['dentiste'])
def afficher_radio_patient(request):
	context = {}
	if request.method =="POST":
		id_patient = request.POST.get('patient')
		nom = Patient.objects.get(id=id_patient).nom
		prenom = Patient.objects.get(id=id_patient).prenom


	context['radio_liste'] = Radio.objects.filter(patient=id_patient)
	context['patient'] = id_patient
	context['nom'] = nom
	context['prenom'] = prenom
	return render(request, "liste-radio-patient.html", context)







