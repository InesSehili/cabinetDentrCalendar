from django.shortcuts import render, redirect
from traitements.forms import TraitementForm, form_validation_error
from django.contrib import messages
from consultations.models import Consultation
from dents.models import Dent
from traitements.models import Traitement
from patients.models import Patient
import decimal
from django.contrib.auth.decorators import login_required
from core.decorators import allowed_users

# Create your views here.
@login_required(login_url="/login/")
@allowed_users(allowed_roles=['dentiste'])
def formulaire_creation_traitement(request):
	context = {}
	if request.method =="POST":
		id_consultation = request.POST.get('id')
		print('id' + id_consultation)
		nom_patient = request.POST.get('nom')
		print('nom ' + nom_patient)
		prenom_patient = request.POST.get('prenom')
		print('prenom ' + prenom_patient)
	consultation=Consultation.objects.get(id=id_consultation)
	print("id consultation= ", consultation.id)
	list_traitement = Traitement.objects.filter(consultation=id_consultation)
	e_c_t_consultation =Consultation.objects.get(id=id_consultation).estimation_du_coût_de_traitement

	print(list_traitement)
	context['list_traitement'] = list_traitement
	context['dent_list'] =  Dent.objects.all().values()
	context['consultation'] = consultation
	context['nom'] = nom_patient
	context['prenom'] = prenom_patient
	context['e_c_t_consultation'] = e_c_t_consultation
	context['espace'] = "- "
	return render(request, "ajouter-traitement.html", context)

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['dentiste'])
def ajouter_traitement(request):
	context = {}
	if request.method =="POST":
		etat_traitement = request.POST.get('etat_traitement')
		print("etat_traitement" + etat_traitement)
		prix_traitement = request.POST.get('prix_traitement')
		print("prix_traitement" + prix_traitement)
		obj_consultation = request.POST.get('consultation')
		print("id" + obj_consultation)
		nom_patient = request.POST.get('nom')
		prenom_patient = request.POST.get('prenom')
		print("obj_consultation = "+ obj_consultation)
		consultation=Consultation.objects.get(id=obj_consultation)
		id_patient = consultation.patient.id
		print("id patient = ", id_patient)
		context['dent_list'] =  Dent.objects.all().values()
		context['consultation'] = consultation
		context['nom'] = nom_patient
		context['prenom'] = prenom_patient
		form = TraitementForm(request.POST or None)
		if form.is_valid():
			print("form is valid")
			f= form.save()
			if etat_traitement == "Valider":
				last_traitement = Traitement.objects.last().id
				Traitement.objects.filter(id=last_traitement).update(reste_traitement=prix_traitement)

				premier_total_payement= Patient.objects.get(id=id_patient).total_payement
				reste_paye_patient= Patient.objects.get(id=id_patient).reste_paye 
				print("premier_total_payement", premier_total_payement)
				Patient.objects.filter(id=id_patient).update(total_payement=premier_total_payement+decimal.Decimal(prix_traitement))
				Patient.objects.filter(id=id_patient).update(reste_paye =reste_paye_patient+decimal.Decimal(prix_traitement))
			premier_e_c_t_patient = Patient.objects.get(id=id_patient).estimation_du_coût_de_traitement
			premier_e_c_t_consultation = Consultation.objects.get(id=obj_consultation).estimation_du_coût_de_traitement
		
			Patient.objects.filter(id=id_patient).update(estimation_du_coût_de_traitement=premier_e_c_t_patient+int(prix_traitement))
			Consultation.objects.filter(id=obj_consultation).update(estimation_du_coût_de_traitement=premier_e_c_t_consultation+int(prix_traitement))

			Consultation.objects.filter(id=obj_consultation).update(traitement_existe=True)
			print(f)
			context['list_traitement'] = Traitement.objects.filter(consultation=obj_consultation)
			e_c_t_consultation =Consultation.objects.get(id=obj_consultation).estimation_du_coût_de_traitement
			context['e_c_t_consultation'] = e_c_t_consultation
			context['espace'] = "- "
			messages.success(request, 'Traitement a été bien ajouté')
			return render(request, "ajouter-traitement.html", context)
		else:
			print("form is NOT valid")
			context['list_traitement'] = Traitement.objects.filter(consultation=obj_consultation)
			e_c_t_consultation =Consultation.objects.get(id=obj_consultation).estimation_du_coût_de_traitement
			context['e_c_t_consultation'] = e_c_t_consultation
			context['espace'] = "- "
			messages.error(request, "Prix traitement erroné")
			return render(request, "ajouter-traitement.html", context)
	return render(request, "ajouter-traitement.html", context)
@login_required(login_url="/login/")
@allowed_users(allowed_roles=['dentiste'])
def valider_traitement(request):
	context = {}
	if request.method =="POST":
		id_consultation = request.POST.get('consultation')
		print("id"+id_consultation)
		nom_patient = request.POST.get('nom')
		prenom_patient = request.POST.get('prenom')
		id_traitement = request.POST.get('id_traitement')
		prix_traitement = request.POST.get('prix_traitement')
		dec_prix_traitement = decimal.Decimal(prix_traitement)
		print("prix", dec_prix_traitement)
		print("id_traitement", id_traitement)
	Traitement.objects.filter(id=id_traitement).update(etat_traitement="Valider")
	Traitement.objects.filter(id=id_traitement).update(reste_traitement=prix_traitement)

	consultation=Consultation.objects.get(id=id_consultation)
	id_patient = consultation.patient.id
	list_traitement = Traitement.objects.filter(consultation=id_consultation)
	premier_total_payement= Patient.objects.get(id=id_patient).total_payement
	reste_paye_patient= Patient.objects.get(id=id_patient).reste_paye 
	print("premier_total_payement", premier_total_payement)
	Patient.objects.filter(id=id_patient).update(total_payement=premier_total_payement+dec_prix_traitement)
	Patient.objects.filter(id=id_patient).update(reste_paye =reste_paye_patient+decimal.Decimal(prix_traitement))
	# premier_e_c_t_consultation = Consultation.objects.get(id=obj_consultation).estimation_du_coût_de_traitement
	# Consultation.objects.filter(id=id_consultation ).update(estimation_du_coût_de_traitement=premier_e_c_t_consultation+int(prix_traitement))



	context['list_traitement'] = list_traitement
	context['dent_list'] =  Dent.objects.all().values()
	context['consultation'] = consultation
	context['nom'] = nom_patient
	context['prenom'] = prenom_patient
	e_c_t_consultation =Consultation.objects.get(id=id_consultation).estimation_du_coût_de_traitement
	context['e_c_t_consultation'] = e_c_t_consultation
	context['espace'] = "- "
	return render(request, "ajouter-traitement.html", context)
@login_required(login_url="/login/")
@allowed_users(allowed_roles=['dentiste'])
def annuler_traitement(request):
	context = {}
	if request.method =="POST":
		id_consultation = request.POST.get('consultation')
		etat_traitement = request.POST.get('etat_traitement')
		print("etat_traitement",etat_traitement)
		prix_traitement = request.POST.get('prix_traitement')
		nom_patient = request.POST.get('nom')
		prenom_patient = request.POST.get('prenom')
		id_traitement = request.POST.get('id_traitement')
		print("id_traitement", id_traitement)
		id_traitement = request.POST.get('id_traitement')
	Traitement.objects.filter(id=id_traitement).update(etat_traitement="Annuler")
	

	consultation=Consultation.objects.get(id=id_consultation)
	id_patient = consultation.patient.id
	list_traitement = Traitement.objects.filter(consultation=id_consultation)
	premier_total_payement= Patient.objects.get(id=id_patient).total_payement
	reste_paye_patient= Patient.objects.get(id=id_patient).reste_paye 
	premier_e_c_t_consultation = Consultation.objects.get(id=id_consultation).estimation_du_coût_de_traitement
	# if etat_traitement == 'Valider':
	# 	Patient.objects.filter(id=id_patient).update(total_payement=premier_total_payement- decimal.Decimal(prix_traitement))
	# 	Patient.objects.filter(id=id_patient).update(reste_paye=reste_paye_patient- decimal.Decimal(prix_traitement))
	Consultation.objects.filter(id=id_consultation).update(estimation_du_coût_de_traitement=premier_e_c_t_consultation-decimal.Decimal(prix_traitement))



	context['list_traitement'] = list_traitement
	context['dent_list'] =  Dent.objects.all().values()
	context['consultation'] = consultation
	context['nom'] = nom_patient
	context['prenom'] = prenom_patient
	context['espace'] = "- "

	e_c_t_consultation =Consultation.objects.get(id=id_consultation).estimation_du_coût_de_traitement
	context['e_c_t_consultation'] = e_c_t_consultation
	return render(request, "ajouter-traitement.html", context) 



@login_required(login_url="/login/")
@allowed_users(allowed_roles=['dentiste'])
def supprimer_traitement(request):
	context = {}
	if request.method =="POST":
		prix_traitement = request.POST.get('prix_traitement')
		dec_prix_traitement = decimal.Decimal(prix_traitement)
		etat_traitement = request.POST.get('etat_traitement')
		print("etat_traitement",etat_traitement)
		id_consultation = request.POST.get('consultation')
		print("id"+id_consultation)
		consultation=Consultation.objects.get(id=id_consultation)
		nom_patient = request.POST.get('nom')
		prenom_patient = request.POST.get('prenom')
		id_traitement = request.POST.get('id_traitement')
		print("id_traitement", id_traitement)

	t = Traitement.objects.get(id=id_traitement)
	if etat_traitement =='Valider':
		if t.prix_payer_traitement >0:
			messages.error(request, "ce traitement est deja payé vous pouvez pas le supprimer")
		else:
			premier_e_c_t_consultation = Consultation.objects.get(id=id_consultation).estimation_du_coût_de_traitement
			Consultation.objects.filter(id=id_consultation).update(estimation_du_coût_de_traitement=premier_e_c_t_consultation-decimal.Decimal(prix_traitement))
			consultation=Consultation.objects.get(id=id_consultation)
			id_patient = consultation.patient.id
			list_traitement = Traitement.objects.filter(consultation=id_consultation)
			premier_total_payement= Patient.objects.get(id=id_patient).total_payement
			reste_paye_patient= Patient.objects.get(id=id_patient).reste_paye 
			print("premier_total_payement", premier_total_payement)
			Patient.objects.filter(id=id_patient).update(total_payement=premier_total_payement-dec_prix_traitement)
			Patient.objects.filter(id=id_patient).update(reste_paye =reste_paye_patient-decimal.Decimal(prix_traitement))
			t.delete()


	if etat_traitement =='A faire':
		premier_e_c_t_consultation = Consultation.objects.get(id=id_consultation).estimation_du_coût_de_traitement
		Consultation.objects.filter(id=id_consultation).update(estimation_du_coût_de_traitement=premier_e_c_t_consultation-decimal.Decimal(prix_traitement))
		t.delete()	
	if etat_traitement =='Annuler':
		t.delete()

	context['dent_list'] =  Dent.objects.all().values()
	context['consultation'] = consultation
	context['nom'] = nom_patient
	context['prenom'] = prenom_patient
	context['list_traitement'] = Traitement.objects.filter(consultation=id_consultation)
	e_c_t_consultation =Consultation.objects.get(id=id_consultation).estimation_du_coût_de_traitement
	context['e_c_t_consultation'] = e_c_t_consultation
	context['espace'] = "- "
	return render(request, "ajouter-traitement.html", context) 






                                                     













