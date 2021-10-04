from django.shortcuts import render, redirect
from fournisseurs.forms import FournisseurForm,  form_validation_error
from fournisseurs.models import Fournisseur
from django.contrib import messages
from patients.models import Patient
from django.utils.timezone import datetime 
import datetime as dt
from payements.models import Payement
from depenses.models import Depense
from employes.models import Employee
from django.contrib.auth.decorators import login_required
from core.decorators import allowed_users


# Create your views here.

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['dentiste'])
def ajouter_fournisseur(request):
	context = {}
	context['segment'] = 'fournisseur'
	if request.method =="POST":
		form = FournisseurForm(request.POST or None)
		if form.is_valid():
			print("form is valid")
			form.save()
			messages.success(request, 'Fournisseur a été bien crée')

		else:
			messages.error(request, form_validation_error(form))
	context['list_fournisseur'] = Fournisseur.objects.all().values().order_by('updated_at')
   
	return render(request, 'ajouter-fournisseur.html', context)




@login_required(login_url="/login/")
@allowed_users(allowed_roles=['dentiste'])
def statistique(request):
	context = {}
	context['segment'] = 'stat'
	revenu_entre = 0
	depense_entre = 0
	if request.method=="POST":
		voir= request.POST.get("voir")
		if voir =="revenue":
			date_debut_str = request.POST.get('date_debut')
			print("date de debut",date_debut_str )
			date_fin_str = request.POST.get('date_fin')
			print(" date_fin", date_fin_str)
			date_debut = dt.datetime.strptime(date_debut_str, '%Y-%m-%d')
			date_fin = dt.datetime.strptime(date_fin_str, '%Y-%m-%d')
			print("date_debut", date_debut)
			print("date_fin", date_fin)
			if date_debut > date_fin:
				messages.error(request, "Date de debut ou de fin erroné")
			else :
				list_payement_entre = Payement.objects.filter(created_at__date__range=[date_debut, date_fin])
				if list_payement_entre.count() !=0:
					for payement in list_payement_entre:
						revenu_entre = revenu_entre + payement.prix_payer
				context['revenu_entre'] = revenu_entre
				print('revenu_entre',revenu_entre )
				context['date_debut'] = date_debut_str 
				context['date_fin'] = date_fin_str
		if voir =="depense":
			date_debut_str_depense = request.POST.get('date_debut_depense')
			print("date de debut_depense",date_debut_str_depense )
			date_fin_str_depense = request.POST.get('date_fin_depense')
			print(" date_fin_depense", date_fin_str_depense)
			date_debut_depense = dt.datetime.strptime(date_debut_str_depense, '%Y-%m-%d')
			date_fin_depense = dt.datetime.strptime(date_fin_str_depense, '%Y-%m-%d')
			print("date_debut_depense", date_debut_depense)
			print("date_fin_depense", date_fin_depense)
			if date_debut_depense > date_fin_depense:
				messages.error(request, "Date de debut ou de fin erroné")

			else :
				list_depense_entre = Depense.objects.filter(created_at__date__range=[date_debut_depense, date_fin_depense])
				if list_depense_entre.count() !=0:
					for depense in list_depense_entre:
						depense_entre = depense_entre + depense.prix_sortie
				context['depense_entre'] = depense_entre
				print('depense_entre',depense_entre )
				context['date_debut_depense'] = date_debut_str_depense 
				context['date_fin_depense'] = date_fin_str_depense





	reste_total_patient = 0
	reste_de_fournisseur = 0
	revenu_semaine = 0
	revenu_mois = 0
	revenu_total = 0
	depense_total = 0
	
	depense_fournisseur_par_mois  = 0
	depenses_fournisseur = 0
	depense_autre = 0
	depense_employes = 0
	date = dt.date.today()
	start_week = date - dt.timedelta(date.weekday()+1)
	end_week = start_week + dt.timedelta(7)
	list_patient = Patient.objects.all()


	
	list_payement = Payement.objects.all()
	list_depense = Depense.objects.all()
	list_payement_semaine = Payement.objects.filter(created_at__date__range=[start_week, end_week])
	list_payement_mois= Payement.objects.filter(created_at__gte=datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0))
	list_depense_fournisseur_par_mois = Depense.objects.filter(raison_payement='fournisseur').filter(created_at__gte=datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0))
	list_depense_fournisseur =  Depense.objects.filter(raison_payement='fournisseur')
	list_depense_employes =  Depense.objects.filter(raison_payement='Employés')
	list_depense_autre =  Depense.objects.filter(raison_payement='Autre')
	list_fournisseur = Fournisseur.objects.all()
	context ['nb_patient'] = list_patient.count()

	if list_patient.count() != 0:
		context['date_du_dernier_patient_ajouter'] = Patient.objects.last().created_at
		for p in list_patient:
			reste_total_patient = reste_total_patient+ p.reste_paye

	if list_fournisseur.count() !=0:
		for f in list_fournisseur:
			reste_de_fournisseur = f.reste_paye+ reste_de_fournisseur


	# if list_payement_semaine.count() !=0:
	# 	for payement in list_payement_semaine:
	# 		revenu_semaine = revenu_semaine+ payement.prix_payer

	# if list_payement_mois.count() !=0:
	# 	for payement in list_payement_mois:
	# 		revenu_mois = revenu_mois + payement.prix_payer

	if list_payement.count() !=0:
		for payement in list_payement:
			revenu_total = revenu_total+ payement.prix_payer

	if list_depense.count() !=0:
		for depense in list_depense:
			depense_total = depense_total+ depense.prix_sortie




	# if list_depense_fournisseur_par_mois.count() !=0:
	# 	for depense in list_depense_fournisseur_par_mois:
	# 		depense_fournisseur_par_mois = depense_fournisseur_par_mois + depense.prix_sortie



	if list_depense_fournisseur.count() !=0:
		for depense in list_depense_fournisseur:
			print("prix de pense = ", depense.prix_sortie)
			depenses_fournisseur = depenses_fournisseur + depense.prix_sortie

	if list_depense_employes.count() !=0:
		for depense in list_depense_employes:
			print("prix de depense", depense.prix_sortie)
			depense_employes = depense_employes + depense.prix_sortie

	if list_depense_autre.count() !=0:
		for depense in list_depense_autre:
			print("prix de depense", depense.prix_sortie)
			depense_autre = depense_autre + depense.prix_sortie







	# context['revenu_semaine'] = revenu_semaine
	# context['revenu_mois'] = revenu_mois
	context['revenu_total'] = revenu_total
	context['depense_total'] = depense_total

	# context['depense_mois_fournisseur'] = depense_fournisseur_par_mois


	context['depense_fournisseur'] = depenses_fournisseur
	context['depense_autre'] = depense_autre
	context['depense_employes'] = depense_employes



	context['to_day'] = date

	context['start_week'] = start_week

	context['end_week'] = end_week

	context['month'] = datetime.now().strftime('%B')
	context['reste_total_patient'] = reste_total_patient
	context['reste_de_fournisseur'] = reste_de_fournisseur
	if list_payement.count() !=0:
		context['date_du_dernier_payement'] = Payement.objects.last().created_at

	context['list_fournisseur'] = Fournisseur.objects.all().values().order_by('updated_at')
	context['list_employee'] = Employee.objects.all().values().order_by('updated_at')
	return render(request, 'statistique.html', context)





@login_required(login_url="/login/")
@allowed_users(allowed_roles=['dentiste'])
def liste_fournisseur(request):
	context = {}
	context['segment'] = 'fournisseur'
	depenses_fournisseur = 0
	list_depense_fournisseur =  Depense.objects.filter(raison_payement='fournisseur')


	if list_depense_fournisseur.count() !=0:
		for depense in list_depense_fournisseur:
			print("prix de pense = ", depense.prix_sortie)
			depenses_fournisseur = depenses_fournisseur + depense.prix_sortie
	context['list_fournisseur'] = Fournisseur.objects.all().values().order_by('updated_at')
	context['depense_fournisseur'] = depenses_fournisseur
	context['list_depense_fournisseur'] =  Depense.objects.filter(raison_payement='fournisseur').order_by('updated_at').reverse()
	

	return render(request, 'liste-fournisseur.html', context)

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['dentiste'])
def supprimer_fournisseur(request):
	context = {}
	context['segment'] = 'fournisseur'
	depenses_fournisseur = 0
	if request.method=="POST":
		fournisseur = request.POST.get("fournisseur")


	f = Fournisseur.objects.get(id=fournisseur).delete()
	#les fournisseur et les achats mais il reste les depenses
	d = Depense.objects.filter(raison_payement="fournisseur").filter(id_raison=fournisseur)
	print(d)
	d.delete()
	list_depense_fournisseur =  Depense.objects.filter(raison_payement='fournisseur')
	if list_depense_fournisseur.count() !=0:
		for depense in list_depense_fournisseur:
			print("prix de pense = ", depense.prix_sortie)
			depenses_fournisseur = depenses_fournisseur + depense.prix_sortie

	context['list_fournisseur'] = Fournisseur.objects.all().values().order_by('updated_at')
	context['depense_fournisseur'] = depenses_fournisseur
	context['list_depense_fournisseur'] =  Depense.objects.filter(raison_payement='fournisseur').order_by('updated_at')
	return render(request, 'liste-fournisseur.html', context)












 