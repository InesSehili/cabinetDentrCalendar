from django.shortcuts import render, redirect
from patients.forms import PatientForm, form_validation_error
from patients.models import Patient
from django.contrib import messages
from consultations.models import Consultation
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

@login_required(login_url="/login/")
def ajouter_patient(request):
	if request.method =="POST":
		nom_patient = request.POST.get('nom')
		prenom_patient = request.POST.get('prenom')
		patients = Patient.objects.filter(nom=nom_patient).filter(prenom = prenom_patient)
		print("**********", patients)
		if patients:
			messages.error(request, "Il exite déja un patient avec le méme nom et prenom")
			return render(request, 'ajouter-patient.html', {})


		form = PatientForm(request.POST or None)
		if form.is_valid():
			print("form is valid")
			patient = form.save()
			messages.success(request, 'Patient a été bien crée')
			return render(request, 'ajouter-patient.html', {})
		else:
			messages.error(request, form_validation_error(form))
	return render(request, 'ajouter-patient.html', {})

@login_required(login_url="/login/")
def liste_patient(request):
	context = {}
	context['segment'] = 'patients'
	context['patient_list'] = Patient.objects.filter(archiver=False).values().order_by('updated_at').reverse()
	
	return render(request, "liste-patient.html", context)
@login_required(login_url="/login/")
def liste_patient_payees(request):
	context = {}
	context['patient_list'] = Patient.objects.filter(archiver=False).filter(reste_paye=0).values().order_by('updated_at')
	return render(request, "liste-patient.html", context)
@login_required(login_url="/login/")
def liste_patient_non_payees(request):
	context = {}
	context['patient_list'] = Patient.objects.filter(archiver=False).exclude(reste_paye=0).values().order_by('updated_at')
	return render(request, "liste-patient.html", context)

@login_required(login_url="/login/")
def liste_patient_archiver(request):
	context = {}
	context['patient_list'] = Patient.objects.filter(archiver=True).values().order_by('updated_at')
	return render(request, "liste-patient-archives.html", context)

@login_required(login_url="/login/")
def archiver_patient(request):
	context = {}
	if request.method =="POST":
		id_patient = request.POST.get('id')
		print(id_patient)
		Patient.objects.filter(id=id_patient).update(archiver=True)
		print("Patient archivé")
	context['patient_list'] = Patient.objects.filter(archiver=False).values().order_by('id').reverse()
	return render(request, "liste-patient.html", context)
@login_required(login_url="/login/")
def desarchiver_patient(request):
	context = {}
	if request.method =="POST":
		id_patient = request.POST.get('id')
		print(id_patient)
		Patient.objects.filter(id=id_patient).update(archiver=False)
		print("Patient archivé")
	context['patient_list'] = Patient.objects.filter(archiver=False).values().order_by('id').reverse()
	return render(request, "liste-patient.html", context)
@login_required(login_url="/login/")
def afficher_detail_patient(request):
	context = {}
	if request.method =="POST":
		id_patient = request.POST.get('id')
		profession = request.POST.get('profession')
		nom_patient = request.POST.get('nom')
		print(nom_patient)
		prenom_patient = request.POST.get('prenom')
		date_naissance_patient = request.POST.get('date_naissance')
		print(date_naissance_patient)
		sexe_patient = request.POST.get('sexe')
		adresse_patient = request.POST.get('adresse')
		numero_tel_patient = request.POST.get('numero_tel')
		email_patient = request.POST.get('email')
		ville_patient = request.POST.get('ville')
		created_at_patient = request.POST.get('created_at')
		#p = Patient.objects.get(id=id_patient)
		fiche_medical = Patient.objects.get(id = id_patient).fiche_medical
		print(fiche_medical)

	context = {
	        "id" : id_patient,
	        "nom" : nom_patient,
	        "prenom" : prenom_patient,
	        "date_naissance" : date_naissance_patient,
	        "sexe" : sexe_patient,
	        "adresse" : adresse_patient,
	        "numero_tel" : numero_tel_patient,
	        "email" : email_patient,
	        "ville" : ville_patient,
	        "profession" : profession,
	        "created_at" : created_at_patient,
	        "fiche_medical" : Patient.objects.get(id = id_patient).fiche_medical,
	          }
	return render(request, 'detail-patient.html', context)
@login_required(login_url="/login/")
def supprimer_patient(request):
	context = {}
	if request.method =="POST":
		id_patient = request.POST.get('id')
		p=Patient.objects.get(id=id_patient)
		p.delete()

		context['patient_list'] = Patient.objects.filter(archiver=True).values().order_by('id').reverse()
		return render(request, 'liste-patient-archives.html', context)



















