from django.shortcuts import render, redirect
from consultations.forms import ConsultationForm, form_validation_error
from consultations.models import Consultation
from django.contrib import messages
from patients.models import Patient
import decimal
from ordonances.models import Ordonance
from traitements.models import Traitement
from django.contrib.auth.decorators import login_required
from core.decorators import allowed_users


# Create your views here.

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['dentiste'])
def ajouter_consultation(request):
	context = {}
	if request.method =="POST":
		patient = request.POST.get('p')
		prix_defini = request.POST.get('prix_defini')
		print(prix_defini)   
		prix_paye = request.POST.get('prix_paye')
		print(prix_paye)
		rest = int(prix_defini) - int(prix_paye)
		print(rest)
		print("patient = "+patient)
		p = Patient.objects.get(id = patient)
		form = ConsultationForm(request.POST or None)
		if form.is_valid():
			print("form is valid")
			consultation = form.save()
			last_consultation = Consultation.objects.last().id
			print(last_consultation)
			Consultation.objects.filter(id=last_consultation).update(patient=p)

			Consultation.objects.filter(id=last_consultation).update(reste=rest)
			print( Consultation.objects.last())
			### prix de toutes les consultation du patient ##
			consultations_patient = Consultation.objects.filter(patient=p)
			#modification total payement
			premier_total_payement= Patient.objects.get(id=patient).total_payement
			reste_paye_patient= Patient.objects.get(id=patient).reste_paye
			print("premier_total_payement", premier_total_payement)
			Patient.objects.filter(id=patient).update(total_payement=premier_total_payement+decimal.Decimal(prix_defini))
			Patient.objects.filter(id=patient).update(reste_paye =reste_paye_patient+decimal.Decimal(prix_defini))

            # Fin modification total payement
			
			Patient.objects.filter(id=patient).update(consultation_existe=True)

			messages.success(request, 'Consultaion a été bien crée')
			consultation_liste_patient = Consultation.objects.filter(patient = p)
			context['consultation_list_patient'] = consultation_liste_patient
			context['id'] = p.id
			context['nom'] = p.nom 
			context['prenom'] = p.prenom
		 
			return render(request, 'liste-consultation-patient.html', context)
		else:
			messages.error(request, "Le prix de consultation doit etre positif")
			context['patient_list'] = Patient.objects.filter(archiver=False).values().order_by('updated_at')
			return render(request, "liste-patient.html", context)
	return render(request, 'detail-patient.html', {})

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['dentiste'])
def modifier_prix_consultation(request):
	context = {}
	prix_consultations = 0
	prix_consultations_paye=0

	if request.method =='POST':
		id_consultaion = request.POST.get('id')
		print(id_consultaion)
		prix_defini = request.POST.get('prix_defini')
		prix_paye = request.POST.get('prix_paye')
	print(prix_defini)
	print(prix_paye)
	prix_defini_consultation = Consultation.objects.get(id=id_consultaion).prix_defini
	prix_paye_consultation =  Consultation.objects.get(id=id_consultaion).prix_paye
	if decimal.Decimal(prix_paye) <0 or decimal.Decimal(prix_defini)<0 or decimal.Decimal(prix_defini)<prix_paye_consultation or decimal.Decimal(prix_paye) >prix_defini_consultation or decimal.Decimal(prix_paye) > decimal.Decimal(prix_defini):
		messages.error(request, "vous avez entré un prix erroné ressayez une autre fois")
		context['consultation_list'] = Consultation.objects.all().order_by('updated_at')
		return render(request, 'liste-consultation.html', context)
	Consultation.objects.filter(id=id_consultaion).update(prix_defini= prix_defini)
	Consultation.objects.filter(id=id_consultaion).update(prix_paye= prix_paye)

	Consultation.objects.filter(id=id_consultaion).update(reste=float( prix_defini)- float(prix_paye))
	p=Consultation.objects.get(id=id_consultaion).patient.id
	print("id patient = ", p)

	### prix de toutes les consultation du patient ##
	consultations_patient = Consultation.objects.filter(patient=p)
	for c in consultations_patient:
		prix_consultations = prix_consultations + c.prix_defini
		prix_consultations_paye = prix_consultations_paye + c.prix_paye
	print("prix total de toutes les consultations = ", prix_consultations)
	print("prix_cosultations_paye = ", prix_consultations_paye)
	reste =prix_consultations - prix_consultations_paye
	print("reste à paye = ", reste)
	Patient.objects.filter(id=p).update(total_payement=prix_consultations)
	Patient.objects.filter(id=p).update(prix_paye=prix_consultations_paye)
	Patient.objects.filter(id=p).update(reste_paye=reste)



	context['consultation_list'] = Consultation.objects.all().order_by('updated_at')
	return render(request, 'liste-consultation.html', context)



	
@login_required(login_url="/login/")
@allowed_users(allowed_roles=['dentiste'])
def modifier_consultation(request):
	if request.method =='POST':
		nom = request.POST.get('nom')
		print( "mon nom est:",nom)
		prenom = request.POST.get('prenom')
		print("mon prenom est",prenom)
		id_consultaion = request.POST.get('id')
		print("my ID est",id_consultaion)
		consultation = Consultation.objects.get(id = id_consultaion)
		print(consultation.patient.nom)
		print(consultation.prix_defini)
		print(consultation.prix_paye)
		print(consultation.reste)

	context = {

	     "id" : id_consultaion,
	     "nom" : consultation.patient.nom,
	     "prenom" : consultation.patient.prenom,
	     "prix_defini" : consultation.prix_defini,
	     "prix_paye" : consultation.prix_paye,
	     "reste" : consultation.reste,
	     "date_consultation": consultation.created_at}
	return render(request, 'modifier-consultation.html', context)


@login_required(login_url="/login/")
@allowed_users(allowed_roles=['dentiste'])
def liste_consultation(request):
	context = {}
	context['segment'] = 'consultations'
	context['consultation_list'] = Consultation.objects.all().order_by('updated_at')
	return render(request, "liste-consultation.html", context)
@login_required(login_url="/login/")
@allowed_users(allowed_roles=['dentiste'])
def formulaire_creation_consultation(request):
	context = {}
	if request.method =="POST":
		id_patient = request.POST.get('id')
		nom_patient = request.POST.get('nom')
		print("nom =", nom_patient)
		prenom_patient = request.POST.get('prenom')
		print(" prenom =", prenom_patient)
		print("id patient = ",id_patient)
	
	context['patient'] =id_patient
	context['nom'] =nom_patient
	context['prenom'] =prenom_patient

	return render(request, "ajouter-consultation.html", context)

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['dentiste'])
def liste_consultation_patient(request):
	context = {}
	if request.method =="POST":
		id_patient = request.POST.get('id')
		print("pssssid", id_patient)
		nom_patient = request.POST.get('nom')
		print("pssssssssnom",nom_patient)
		prenom_patient = request.POST.get('prenom')
		print("prenom", prenom_patient)
	consultation_liste_patient = Consultation.objects.filter(patient = id_patient)
	context['consultation_list_patient'] = consultation_liste_patient
	context['nom'] = nom_patient
	context['prenom'] = prenom_patient
	context['id'] = id_patient
	return render(request, "liste-consultation-patient.html", context)
@login_required(login_url="/login/")
@allowed_users(allowed_roles=['dentiste'])
def supprimer_consultation(request):
	context = {}
	if request.method =="POST":
		id_consultaion = request.POST.get('id')
		print("id_consultaion",id_consultaion)
		id_patient = request.POST.get('patient')
		print("id_patient = ", id_patient)
		consultation = Consultation.objects.get(id=id_consultaion)
		prix_consultation = consultation.prix_defini
		prix_paye_consultation = consultation.prix_paye
		try:
			ordonance_consultation = Ordonance.objects.get(consultation_id= id_consultaion)
			diagnostique_consultation = Diagnostique.objects.get(consultation= id_consultaion)
			traitement_consultation = Traitement.objects.filter(consultation = id_consultaion)
			
		except Exception as e:
			ordonance_consultation = None
			traitement_consultation = None
			diagnostique_consultation = None


		if prix_paye_consultation > 0 or ordonance_consultation or traitement_consultation or diagnostique_consultation:
			messages.error(request, "vous pouvez pas supprimer cette consultation")
		else:
			consultation.delete()
			#modification total payement
			premier_total_payement= Patient.objects.get(id=int(id_patient)).total_payement
			reste_paye_patient= Patient.objects.get(id=int(id_patient)).reste_paye
			print("premier_total_payement", premier_total_payement)
			Patient.objects.filter(id=id_patient).update(total_payement=premier_total_payement- prix_consultation)
			Patient.objects.filter(id=id_patient).update(reste_paye =reste_paye_patient- prix_consultation)

		
		
		
	c = Consultation.objects.filter(patient=id_patient)
	if not c.exists():
		Patient.objects.filter(id=id_patient).update(consultation_existe=False)
	consultations = Consultation.objects.all().order_by('id').reverse()
	context['consultation_list'] = consultations
	return render(request, "liste-consultation.html", context)

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['dentiste'])
def liste_consultation_payees(request):
	context = {}
	context['segment'] = 'consultations'
	context['consultation_list']  = Consultation.objects.filter(reste=0).values().order_by('id').reverse()
	return render(request, "liste-consultation.html", context)
@login_required(login_url="/login/")
@allowed_users(allowed_roles=['dentiste'])
def liste_consultation_non_payees(request):
	context = {}
	context['segment'] = 'consultations'
	context['consultation_list']  = Consultation.objects.exclude(reste=0).values().order_by('id').reverse()
	return render(request, "liste-consultation.html", context)

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['dentiste'])
def liste_consultation_patient_payees(request):
	context = {}
	if request.method=="POST":
		id_patient = request.POST.get('id')
		print('id'+ id_patient)
		nom_patient = request.POST.get('nom')
		print("pssssssssnom",nom_patient)
		prenom_patient = request.POST.get('prenom')
		print("prenom", prenom_patient)

	context['consultation_list_patient']  = Consultation.objects.filter(reste=0).filter(patient =id_patient)
	c= Consultation.objects.filter(reste=0).filter(patient =id_patient).values().order_by('id').reverse()
	print(c)
	context['id'] = id_patient
	context['nom'] = nom_patient
	context['prenom'] = prenom_patient
	return render(request, "liste-consultation-patient.html", context)
@login_required(login_url="/login/")
@allowed_users(allowed_roles=['dentiste'])
def liste_consultation_patient_non_payees(request):
	context = {}
	if request.method=="POST":
		id_patient = request.POST.get('id')
		print('id'+ id_patient)
		nom_patient = request.POST.get('nom')
		print("pssssssssnom",nom_patient)
		prenom_patient = request.POST.get('prenom')
		print("prenom", prenom_patient)

	context['consultation_list_patient']  = Consultation.objects.exclude(reste=0).filter(patient =id_patient)
	c = Consultation.objects.exclude(reste=0).filter(patient =id_patient).values().order_by('id').reverse()
	print(c)
	
	context['id'] = id_patient
	context['nom'] = nom_patient
	context['prenom'] = prenom_patient
	return render(request, "liste-consultation-patient.html", context)





	