from django.shortcuts import render, redirect
from employes.forms import EmployeeForm, form_validation_error
from django.contrib import messages
from employes.models import Employee
from depenses.models import Depense
from django.contrib.auth.decorators import login_required
from core.decorators import allowed_users




@login_required(login_url="/login/")
@allowed_users(allowed_roles=['dentiste'])
def ajouter_employee(request):
	context = {}
	context['segment'] = 'employe'
	if request.method == "POST":
		form = EmployeeForm(request.POST or None)
		if form.is_valid():
			print("is valid")
			form.save()
			messages.success(request, 'Employee a été bien ajouté')
		else:
			print("is not valid")
			print(form_validation_error(form))
			messages.error(request, "Numero de telephone doit etre unique")
	
	context['list_employee'] = Employee.objects.all().values()
	return render(request, 'ajouter-employee.html', context)


@login_required(login_url="/login/")
@allowed_users(allowed_roles=['dentiste'])
def liste_employe(request):
	context = {}
	context['segment'] = 'employe'
	depenses_employe = 0
	list_depense_employe = Depense.objects.filter(raison_payement='Employés')

	if list_depense_employe.count() !=0:
		for depense in list_depense_employe:
			print("prix de pense = ", depense.prix_sortie)
			depenses_employe = depenses_employe + depense.prix_sortie

	context['list_employee'] = Employee.objects.all().values().order_by('updated_at')
	context['depenses_employe'] = depenses_employe
	context['list_depense_employe'] = Depense.objects.filter(raison_payement='Employés')

	return render(request, 'liste-employe.html', context)

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['dentiste'])
def supprimer_employe(request):
	context = {}
	context['segment'] = 'employe'
	if request.method =="POST":
		employe = request.POST.get("employe")
		print("employe = ", employe)


	d = Depense.objects.filter(raison_payement='Employés').filter(id_raison=employe).delete()
	Employee.objects.get(id=employe).delete()
	print(d)
	context['list_employee'] = Employee.objects.all().values().order_by('updated_at')
	return render(request, 'liste-employe.html', context)





