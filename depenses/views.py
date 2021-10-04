from django.shortcuts import render, redirect
from django.contrib import messages
from depenses.models import Depense
import decimal
from employes.models import Employee
from django.contrib.auth.decorators import login_required
from core.decorators import allowed_users


# Create your views here.
@login_required(login_url="/login/")
@allowed_users(allowed_roles=['dentiste'])
def ajouter_depense(request):
	context = {}
	id_employee=0
	if request.method == "POST":
		prix_sortie = request.POST.get("prix_sortie")
		print("prix_sortie", prix_sortie)
		raison_payement =  request.POST.get("raison_payement")
		print("raison_payement", raison_payement)
		note = request.POST.get("note")
		print("note", note)
		employee = request.POST.get("employee")
		print("employee", employee)
		if employee != None:
			id_employee =  int (employee.split()[0])
			print("id employee", id_employee)
		if decimal.Decimal(prix_sortie) <0:
			messages.error(request, "le prix sorti doit étre superieur ou egal à 0")
			context['list_depense'] = Depense.objects.all().order_by('updated_at')
			return render(request, 'ajouter-depense.html', context)
	depense = Depense(prix_sortie=decimal.Decimal(prix_sortie ),raison_payement=raison_payement, note=note, employee=employee, id_raison=id_employee)
	depense.save()
	messages.success(request, "depense a été bien ajoutée")

	context['list_depense'] = Depense.objects.all().order_by('updated_at')
	return render(request, 'ajouter-depense.html', context)

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['dentiste'])
def formulaire_ajouter_depense(request):
	context = {}
	context['list_depense'] = Depense.objects.filter(raison_payement="Autre").order_by('updated_at')
	return render(request, 'ajouter-depense.html', context)

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['dentiste'])
def formulaire_ajouter_depense_employee(request):
	context = {}
	context['list_depense'] = Depense.objects.filter(raison_payement="Employés")
	list_employe = Employee.objects.all()
	if list_employe.count()==0:
		messages.error(request,"Ajouter d'abord un employés !")
		return render(request, 'ajouter-depense.html', context)
	context['list_employee'] =  Employee.objects.all().values().order_by('updated_at')
	return render(request, 'ajouter-depense-empployee.html', context)
@login_required(login_url="/login/")
@allowed_users(allowed_roles=['dentiste'])
def supprimer_depense(request):
	context = {}
	if request.method =="POST":
		id_depense = request.POST.get("id_depense")
		depense = Depense.objects.get(id=id_depense)
		depense.delete()
		context['list_depense'] = Depense.objects.all().order_by('updated_at')
		return render(request, 'ajouter-depense.html', context)









