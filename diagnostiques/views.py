from django.shortcuts import render, redirect
from diagnostiques.forms import DiagnostiqueForm, form_validation_error
from diagnostiques.models import Diagnostique
from django.contrib import messages
from consultations.models import Consultation
from django.contrib.auth.decorators import login_required
from core.decorators import allowed_users
from cal.models import Event
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
@login_required(login_url="/login/")
@allowed_users(allowed_roles=['dentiste'])
def ajouter_diagnostique(request):
	context = {}
	if request.method =="POST":
		id_consultation = request.POST.get('consultation')
		nom = request.POST.get('nom')
		prenom = request.POST.get('prenom')
		print("nom="+ nom)
		print("prenom"+ prenom)
		print( "id",id_consultation)
		consultation = Consultation.objects.get(id=id_consultation)
		form = DiagnostiqueForm(request.POST or None)
		if form.is_valid():
			print("form is valid")
			diagnostique = form.save()
			Consultation.objects.filter(id=id_consultation).update(diagnostique_existe=True)
			last_diagnostique = Diagnostique.objects.get(consultation=id_consultation)
			consultation = Consultation.objects.get(id = id_consultation)
			context = {
			   "id" : id_consultation,
			   "nom" : nom,
			   "prenom" : prenom,
			   "nom_medecin" : last_diagnostique.nom_medecin,
			   "diagnostique" : last_diagnostique.txt_diagnostique,
			   "observation" : last_diagnostique.observation,
			   "created_at" : last_diagnostique.created_at,
			   "consultation" : consultation,

			}
			messages.success(request, 'Diagnostique a été bien crée')

			return render(request, 'afficher-diagnostique.html', context)
		else:
			messages.error(request, form_validation_error(form))

	return render(request, 'afficher-diagnostique.html', {})

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['dentiste'])
def formulaire_creation_diagnostique(request):
	context = {}
	if request.method =="POST":
		id_consultaion = request.POST.get('id_consultation')
		nom_patient = request.POST.get('nom')
		prenom_patient = request.POST.get('prenom')
		print("nom = ", nom_patient)
		print("prenom = ", prenom_patient)

	context['id_consultation'] = id_consultaion
	context['nom_patient'] = nom_patient
	context['prenom_patient'] = prenom_patient

	return render(request, "ajouter-diagnostique.html", context)
@login_required(login_url="/login/")
@allowed_users(allowed_roles=['dentiste'])
def afficher_diagnostique(request):
	context = {}
	if request.method =="POST":
		id_consultation = request.POST.get('id_consultation')
		print("id_consultation",id_consultation)
		nom = request.POST.get('nom')
		print("nom" , nom)
		prenom = request.POST.get('prenom')
		print("prenom" , nom)
		diagnostique_obj = Diagnostique.objects.get(consultation=id_consultation)
		consultation = Consultation.objects.get(id = id_consultation)
		

	context = {
	     "nom" : nom,
	     "prenom" : prenom,
	     "id" : diagnostique_obj.consultation_id,
	     "diagnostique" : diagnostique_obj.txt_diagnostique,
	     "nom_medecin" : diagnostique_obj.nom_medecin,
	     "observation" : diagnostique_obj.observation,
	     "created_at" : diagnostique_obj.created_at,
	     "consultation" : consultation,


	}
	return render(request, 'afficher-diagnostique.html', context)


# def modifier_diagnostique_formulaire(request):
# 	context = {}
# 	if request.method =="POST":
# 		id_diagnostique= request.POST.get('id')
# 		nom = request.POST.get('nom')
# 		prenom = request.POST.get('prenom')

# 	diagnostique_obj = Diagnostique.objects.get(consultation=id_diagnostique)
# 	context = {
# 	     "nom_patient" : nom,
# 	     "prenom_patient" : prenom,
# 	     "id_consultation" : diagnostique_obj.consultation_id,
# 	     "diagnostique" : diagnostique_obj.diagnostique,
# 	     "nom_medecin" : diagnostique_obj.nom_medecin,
# 	     "observation" : diagnostique_obj.observation,
# 	     "created_at" : diagnostique_obj.created_at,

# 	} 
# 	 return render(request, 'modifier-diagnostique.html', context)


@login_required(login_url="/login/")
@allowed_users(allowed_roles=['dentiste'])
def modifier_diagnostique_formulaire(request):
	context = {}
	if request.method =="POST":
		id_diagnostique= request.POST.get('id')
		nom = request.POST.get('nom')
		prenom = request.POST.get('prenom')
	diagnostique_obj = Diagnostique.objects.get(consultation=id_diagnostique)
	print("observation ="+diagnostique_obj.observation)
	

	context = {
	     "nom_patient" : nom,
	     "prenom_patient" : prenom,
	     "id_consultation" : diagnostique_obj.consultation_id,
	     "diagnostique" : diagnostique_obj.diagnostique,
	     "nom_medecin" : diagnostique_obj.nom_medecin,
	     "observation" : diagnostique_obj.observation,
	     "created_at" : diagnostique_obj.created_at,

	}
	return render(request, 'modifier-diagnostique.html', context)
@login_required(login_url="/login/")
@allowed_users(allowed_roles=['dentiste'])
def supprimer_diagnostique(request):
	context = {}
	if request.method =="POST":
		id_diagnostique = request.POST.get('id')
		id_patient = request.POST.get('id_patient')
		nom = request.POST.get('nom')
		prenom = request.POST.get('prenom')

		print("id _ patient", id_patient)
		diagnostique = Diagnostique.objects.get(consultation=id_diagnostique)
		diagnostique.delete()
		consultation_liste_patient = Consultation.objects.filter(patient = id_patient)
		Consultation.objects.filter(id=id_diagnostique).update(diagnostique_existe=False)
		context['consultation_list_patient'] = consultation_liste_patient
		context['nom'] = nom
		context['prenom'] = prenom
		context['id'] = id_patient

		return render(request, "liste-consultation-patient.html", context)

# @login_required(login_url="/login/")
# def delete_event(request):
#     if request.method =="POST":
#         id_event = request.POST.get('id_event')
#         print( "l'idée de l'evenement est", id_event)
#         print( "*************************/*///////////////////////****************")

    

#     Event.objects.get(id=id_event).delete()

#     url = reverse('cal:calendar')
#     return  HttpResponseRedirect(url)


	









	
 




