from django.shortcuts import render, redirect
from medicaments.forms import MedicamentForm, form_validation_error
from medicaments.models import Medicament
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.decorators import allowed_users

# Create your views here.
@login_required(login_url="/login/")
@allowed_users(allowed_roles=['dentiste'])
def ajouter_medicament(request):
	context = {}
	context['segment'] = 'medicaments'

	if request.method == "POST":
		forme = request.POST.get('forme')
		print("forme", forme)
		form = MedicamentForm(request.POST or None)
		if form.is_valid():
			print("form is valid")
			medicament = form.save()
			messages.success(request, 'Medicament a été bien crée')
			return render(request, 'ajouter-medicament.html', {})
@login_required(login_url="/login/")
@allowed_users(allowed_roles=['dentiste'])
def liste_medicament(request):
	context = {}
	context['segment'] = 'medicaments'
	context['medicament_list'] = Medicament.objects.all().order_by('updated_at')
	return render(request, "liste-medicament.html", context)

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['dentiste'])
def supprimer_medicament(request):
	context = {}
	context['segment'] = 'medicaments'
	if request.method =="POST":
		id_medicament = request.POST.get('id')
		medicament = Medicament.objects.get(id=id_medicament)
		medicament.delete()
	medicaments = Medicament.objects.values().order_by('updated_at')
	context['medicament_list'] = medicaments
	return render(request, "liste-medicament.html", context)
@login_required(login_url="/login/")
@allowed_users(allowed_roles=['dentiste'])
def modifier_medicament_formulaire(request):
	context = {}
	context['segment'] = 'medicaments'
	if request.method =='POST':
		id_medicament = request.POST.get('id')
		nom_medicament = request.POST.get('nom_medicament')
		dose_medicament = request.POST.get('dose')
		forme_medicament = request.POST.get('forme')
	context = {

	   "nom_medicament": nom_medicament,
	   "dose" : dose_medicament,
	   "forme" : forme_medicament,
	   "id" : id_medicament,

	}
	return render(request, 'modifier-medicament.html', context)

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['dentiste'])
def modifier_medicament(request):
	context = {}
	context['segment'] = 'medicaments'
	if request.method =='POST':
		id_medicament = request.POST.get('id')
		nom_medicament = request.POST.get('nom_medicament')
		dose_medicament = request.POST.get('dose')
		forme_medicament = request.POST.get('forme')

	Medicament.objects.filter(id=id_medicament).update(nom_medicament=nom_medicament)
	Medicament.objects.filter(id=id_medicament).update(dose=dose_medicament)
	
	Medicament.objects.filter(id=id_medicament).update(forme=forme_medicament)


	context['medicament_list'] = Medicament.objects.all().order_by('updated_at')
	return render(request, 'liste-medicament.html', context)









