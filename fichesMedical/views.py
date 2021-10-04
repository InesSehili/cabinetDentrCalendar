from django.shortcuts import render, redirect
from patients.models import Patient
from django.contrib import messages
from django.contrib import messages
from fichesMedical.models import FicheMedical 
from fichesMedical.forms import FicheMedicalForm, form_validation_error
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url="/login/")
def formulaire_creation_fiche_medical(request):
	context = {}
	if request.method =="POST":
		id_patient = request.POST.get('id')
		nom_patient = request.POST.get('nom')
		prenom_patient = request.POST.get('prenom')

	context['patient'] = id_patient
	context['nom'] = nom_patient
	context['prenom'] = prenom_patient

	return render(request, "ajouter-fiche-medical.html", context)
@login_required(login_url="/login/")
def ajouter_fiche_medical(request):
	context = {}

	if request.method =="POST":
		id_patient = request.POST.get('id')
		print("id patient du fiche medical" + id_patient)
		p = Patient.objects.get(id=id_patient)

		form = FicheMedicalForm(request.POST or None)
		if form.is_valid():
			print("form is valid")
			fiche_medical = form.save()
			Patient.objects.filter(id=id_patient).update(fiche_medical_existe=True)
			last_fiche_medical = FicheMedical.objects.last().id
			print(last_fiche_medical)
			FicheMedical.objects.filter(id=last_fiche_medical).update(patient=p)
			messages.success(request, 'Fiche medicale a été bien crée')
			context['patient_list'] = Patient.objects.filter(archiver=False).values().order_by('updated_at')

			return render(request, 'liste-patient.html', context)
		else:
			messages.error(request, form_validation_error(form))
	return render(request, 'liste-patient.html', {})
@login_required(login_url="/login/")
def liste_fiche_medical(request):
	context = {}
	context['segment'] = 'fiches_medical'
	context['fiches_medical_list'] = FicheMedical.objects.all()
	return render(request, 'liste-fiche-medical.html', context)
@login_required(login_url="/login/")
def supprimer_fiche_medical(request):
	context = {}
	context['segment'] = 'fiches_medical'
	if request.method =="POST":
		id_fiche_medical = request.POST.get('id')
		id_patient = request.POST.get('id_patient')
		fiche_medical = FicheMedical.objects.get(id=id_fiche_medical)
		fiche_medical.delete()
		Patient.objects.filter(id=id_patient).update(fiche_medical_existe=False)
	context['fiches_medical_list'] = FicheMedical.objects.values().order_by('id').reverse()
	return render(request, 'liste-fiche-medical.html', context)

@login_required(login_url="/login/")
def afficher_fiche_medical(request):
	context = {}
	context['segment'] = 'fiches_medical'
	if request.method =='POST':
		id_patient = request.POST.get('id')
		print("id"+id_patient)
		nom_patient = request.POST.get('nom')
		prenom_patient = request.POST.get('prenom')
	fiche_medical = FicheMedical.objects.get(patient=id_patient)
	print(fiche_medical)
	print(fiche_medical.id)
	print(fiche_medical.antecF)
	print(fiche_medical.antecC)
	print(fiche_medical.antecM)
	print(fiche_medical.antecA)
	print(nom_patient)
	print(prenom_patient)

	context = {
	      "id" : fiche_medical.id,
	      "nom" : nom_patient, 
	      "prenom" : prenom_patient,
	      "antecF" : fiche_medical.antecF,
	      "antecC" : fiche_medical.antecC,
	      "antecM" : fiche_medical.antecM, 
	      "antecA" : fiche_medical.antecA,
	      "groupage" : fiche_medical.groupage,
	      "id_patient" : id_patient,
	      "maladie_axcecie" : fiche_medical.maladie_axcecie,
	      "medication_encours" : fiche_medical.medication_encours,
	      "histoire_de_la_maladie" :fiche_medical.histoire_de_la_maladie,


	}

	return render(request, 'afficher-fiche-medical.html', context)
@login_required(login_url="/login/")
def modifier_fiche_medical(request):
	if request.method =='POST':
		nom = request.POST.get('nom')
		print( "mon nom est:",nom)
		prenom = request.POST.get('prenom')
		print("mon prenom est",prenom)
		id_fiche_medical = request.POST.get('id')
		fiche_medical = FicheMedical.objects.get(id = id_fiche_medical)
	context = {

	     "id" : id_fiche_medical,
	     "nom" : nom,
	     "prenom" : prenom,
	     "groupage" : fiche_medical.groupage,
	     "antecF" : fiche_medical.antecF,
	     "antecC" : fiche_medical.antecC,
	     "antecM" : fiche_medical.antecM,
	     "antecA": fiche_medical.antecA,
	     "maladie_axcecie": fiche_medical.maladie_axcecie,
	     "medication_encours": fiche_medical.medication_encours,
	     "histoire_de_la_maladie": fiche_medical.histoire_de_la_maladie,}
	return render(request, 'modifier-fiche-medical.html', context)

@login_required(login_url="/login/")
def modifier_contenu_fiche_medical(request):
	context = {}
	if request.method =='POST':
		id_fiche_medical = request.POST.get('id')
		print("id",id_fiche_medical)
		groupage = request.POST.get('groupage')
		print('groupage', groupage)
		antecF = request.POST.get('antecF')
		antecC = request.POST.get('antecC')
		antecM = request.POST.get('antecM')
		antecA = request.POST.get('antecA')
		maladie_axcecie = request.POST.get('maladie_axcecie')
		medication_encours = request.POST.get('medication_encours')
		histoire_de_la_maladie = request.POST.get('histoire_de_la_maladie')
	FicheMedical.objects.filter(id=id_fiche_medical).update(groupage=groupage)
	FicheMedical.objects.filter(id=id_fiche_medical).update(antecF=antecF)
	FicheMedical.objects.filter(id=id_fiche_medical).update(antecC=antecC)
	FicheMedical.objects.filter(id=id_fiche_medical).update(antecM=antecM)
	FicheMedical.objects.filter(id=id_fiche_medical).update(antecA=antecA)
	FicheMedical.objects.filter(id=id_fiche_medical).update(maladie_axcecie=maladie_axcecie)
	FicheMedical.objects.filter(id=id_fiche_medical).update(medication_encours=medication_encours)
	FicheMedical.objects.filter(id=id_fiche_medical).update(histoire_de_la_maladie=histoire_de_la_maladie)
	context['patient_list'] = Patient.objects.filter(archiver=False).values().order_by('updated_at')
	return render(request, 'liste-patient.html', context)
















