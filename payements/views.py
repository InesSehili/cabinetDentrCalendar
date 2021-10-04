from django.shortcuts import render, redirect
from django.contrib import messages
from payements.forms import PayementForm, form_validation_error
from patients.models import Patient
from payements.models import Payement
import decimal
from consultations.models import Consultation
from radios.models import  Radio
from traitements.models import Traitement
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url="/login/")
def formulaire_creation_payement(request):
	context = {}
	if request.method =="POST":
		id_patient = request.POST.get('patient')
		print(id_patient)
		nom_patient = request.POST.get('nom')
		print(nom_patient)
		prenom_patient = request.POST.get('prenom')
		print(prenom_patient)
    # context['liste_consultation_non_payees'] =  Consultation.objects.exclude(reste=0).filter(patient =id_patient)
	context['nom'] = nom_patient
	context['prenom'] = prenom_patient
	context['patient'] = id_patient
	context['list_payement'] = Payement.objects.filter(patient=id_patient)
	p=Patient.objects.get(id=id_patient)
	context['p'] = p
	context['liste_consultation_non_payees'] = Consultation.objects.exclude(reste=0).filter(patient=id_patient)
	context['liste_radio_non_payees'] = Radio.objects.exclude(reste=0).filter(patient=id_patient)
	list_consultation = Consultation.objects.filter(patient=id_patient)
	list_traitement = []
	for c in list_consultation:
		list_traitement_par_consultation = Traitement.objects.filter(etat_traitement ="Valider").exclude(reste_traitement=0).filter(consultation=c.id)
		for t in list_traitement_par_consultation:
			list_traitement.append(t)

	print(list_traitement)
	context['liste_traitement_non_payees'] = list_traitement
	return render(request, "ajouter-payement-patient.html", context)

@login_required(login_url="/login/")
def ajouter_payement(request):
	prix_payer_consultation = 0
	reste_consultation = 0
	prix_defini_consultation = 0
	context = {}
	if request.method =="POST":
		id_patient = request.POST.get('patient')
		print(id_patient)
		prix_payer = request.POST.get('prix_payer')
		nom_patient = request.POST.get('nom')
		print(nom_patient)
		
		prenom_patient = request.POST.get('prenom')
		 
		print(prenom_patient)

		payement_de = request.POST.get('payement_de')
		raison_payement = payement_de.split()[0]
		id_raison_payement = payement_de.split()[1]
		print("raison de payement", raison_payement)
		print("id_raison_payement", id_raison_payement)


	prix_total_patient = Patient.objects.get(id=id_patient).total_payement
	prix_paye_patient = Patient.objects.get(id=id_patient).prix_paye
	reste_paye_patient = Patient.objects.get(id=id_patient).reste_paye
	context['list_payement'] = Payement.objects.filter(patient=id_patient)
	context['patient'] = id_patient
	
	
	# list_consultation = Consultation.objects.filter(patient=id_patient)
	# list_traitement = []
	# for c in list_consultation:
	# 	list_traitement_par_consultation = Traitement.objects.filter(etat_traitement ="Valider").exclude(reste_traitement=0).filter(consultation=c.id)
	# 	for t in list_traitement_par_consultation:
	# 		list_traitement.append(t)
	# context['liste_traitement_non_payees'] = list_traitement
	p=Patient.objects.get(id=id_patient)
	context['p'] = p



	if decimal.Decimal(prix_payer) >  reste_paye_patient:
		print("prix payé erroné")
		messages.error(request, "prix payé est superieur du reste de payements")
		context['patient_list'] = Patient.objects.filter(archiver=False).values().order_by('updated_at')
		return render(request, "liste-patient.html", context)
		

	else: 

		if raison_payement == "Consultation" :
			print("oui c une consultation")

			reste_consultation = Consultation.objects.get(id=decimal.Decimal(id_raison_payement)).reste
			print("rest = ", reste_consultation)
			prix_payer_consultation = Consultation.objects.get(id=decimal.Decimal(id_raison_payement)).prix_paye
			print("prix_payer = ", prix_payer_consultation)
			prix_defini_consultation = Consultation.objects.get(id=decimal.Decimal(id_raison_payement)).prix_defini
			print("pris consulttaion", prix_defini_consultation)



			if decimal.Decimal(prix_payer) > reste_consultation:
				messages.error(request, "prix payé de consultation est superieur du reste de payements")
				context['patient_list'] = Patient.objects.filter(archiver=False).values().order_by('updated_at')
				return render(request, "liste-patient.html", context)
		if raison_payement == "Radio":
			print("oui c'est un radio ")
			reste_radio = Radio.objects.get(id=decimal.Decimal(id_raison_payement)).reste
			prix_payer_radio = Radio.objects.get(id=decimal.Decimal(id_raison_payement)).prix_paye
			print("prix_payer = ", prix_payer_radio)
			prix_defini_radio = Radio.objects.get(id=decimal.Decimal(id_raison_payement)).prix_radio
			print("prix_radio", prix_defini_radio)
			if decimal.Decimal(prix_payer) > reste_radio:
				messages.error(request, "prix payé de radio est superieur du reste de payements")
				context['patient_list'] = Patient.objects.filter(archiver=False).values().order_by('updated_at')
				return render(request, "liste-patient.html", context)
				


		if raison_payement =="Traitement":
			print("oui c'est un traitement")
			reste_traitement = Traitement.objects.get(id=decimal.Decimal(id_raison_payement)).reste_traitement
			prix_payer_traitement = Traitement.objects.get(id=decimal.Decimal(id_raison_payement)).prix_payer_traitement
			prix_defini_traitement = Traitement.objects.get(id=decimal.Decimal(id_raison_payement)).prix_traitement


			if decimal.Decimal(prix_payer) > reste_traitement:
				messages.error(request, "prix payé  traitement est superieur du reste de payements")
				context['patient_list'] = Patient.objects.filter(archiver=False).values().order_by('updated_at')
				return render(request, "liste-patient.html", context)


			


		form = PayementForm(request.POST or None)
		if form.is_valid():
			print("form is valid ")
			form.save()
			if raison_payement == "Consultation" :
				Consultation.objects.filter(id=decimal.Decimal(id_raison_payement)).update(prix_paye= prix_payer_consultation+decimal.Decimal(prix_payer))
				dernier_prix_paye = Consultation.objects.get(id=decimal.Decimal(id_raison_payement)).prix_paye
				print("prix payer",dernier_prix_paye)
				print("prix_defini_consultation", prix_defini_consultation)
				Consultation.objects.filter(id=decimal.Decimal(id_raison_payement)).update(reste= prix_defini_consultation-dernier_prix_paye)



			if raison_payement == "Radio":
				Radio.objects.filter(id=decimal.Decimal(id_raison_payement)).update(prix_paye= prix_payer_radio+decimal.Decimal(prix_payer))
				dernier_prix_paye = Radio.objects.get(id=decimal.Decimal(id_raison_payement)).prix_paye
				print("prix payer",dernier_prix_paye)
				print("prix_defini_consultation", prix_defini_radio)
				Radio.objects.filter(id=decimal.Decimal(id_raison_payement)).update(reste= prix_defini_radio-dernier_prix_paye)



			if raison_payement =="Traitement":
				Traitement.objects.filter(id=decimal.Decimal(id_raison_payement)).update(prix_payer_traitement=prix_payer_traitement+decimal.Decimal(prix_payer))
				dernier_prix_paye = Traitement.objects.get(id=decimal.Decimal(id_raison_payement)).prix_payer_traitement 
				Traitement.objects.filter(id=decimal.Decimal(id_raison_payement)).update(reste_traitement= prix_defini_traitement-dernier_prix_paye )



			Patient.objects.filter(id=id_patient).update(prix_paye=prix_paye_patient+ decimal.Decimal(prix_payer) )
			prix_paye_patient_2 = Patient.objects.get(id=id_patient).prix_paye

			Patient.objects.filter(id=id_patient).update(reste_paye=prix_total_patient- prix_paye_patient_2)
			#**********************************************************************
			context['liste_radio_non_payees'] = Radio.objects.exclude(reste=0).filter(patient=id_patient)
			context['liste_consultation_non_payees'] = Consultation.objects.exclude(reste=0).filter(patient=id_patient)

			list_consultation = Consultation.objects.filter(patient=id_patient)
			list_traitement = []
			for c in list_consultation:
				list_traitement_par_consultation = Traitement.objects.filter(etat_traitement ="Valider").exclude(reste_traitement=0).filter(consultation=c.id)
				for t in list_traitement_par_consultation:
					list_traitement.append(t)

			context['liste_traitement_non_payees'] = list_traitement
			

			context['list_payement'] = Payement.objects.filter(patient=id_patient)
			messages.success(request, 'Payement a été bien ajouté')
			return render(request, "ajouter-payement-patient.html", context)

		else:
			context['liste_radio_non_payees'] = Radio.objects.exclude(reste=0).filter(patient=id_patient)
			context['liste_consultation_non_payees'] = Consultation.objects.exclude(reste=0).filter(patient=id_patient)
			list_consultation = Consultation.objects.filter(patient=id_patient)
			list_traitement = []
			for c in list_consultation:
				list_traitement_par_consultation = Traitement.objects.filter(etat_traitement ="Valider").exclude(reste_traitement=0).filter(consultation=c.id)
				for t in list_traitement_par_consultation:
					list_traitement.append(t)
			context['liste_traitement_non_payees'] = list_traitement
			context['list_payement'] = Payement.objects.filter(patient=id_patient)
			print("form is NOT valid")
			messages.error(request, "le prix doit etre superieur ou egal a 0")
			return render(request, "ajouter-payement-patient.html", context)
	
	return render(request, "ajouter-payement-patient.html", context)





