from django.shortcuts import render, get_object_or_404, redirect
from rdvs.forms import RdvForm, form_validation_error
from rdvs.models import Rdv
from django.contrib import messages
# Create your views here.
from django.utils.timezone import datetime 
import datetime as dt
from django.contrib.auth.decorators import login_required
from patients.models import Patient
from typerdvs.models import Typerdv
from cal.models import Event
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect




@login_required(login_url="/login/")
def ajouter_rdv(request):
	context = {}
	context ['segment'] = 'rdvs'
	context['typrrdv_list'] = Typerdv.objects.all()
	if request.method =="POST":
		date_debut_str = request.POST.get('date_rdv')
		print("date de debut",date_debut_str )
		date_fin_str = request.POST.get('date_fin')
		print(" date_fin", date_fin_str)
		date_debut = dt.datetime.strptime(date_debut_str, '%Y-%m-%dT%H:%M')
		date_debut_evenement = date_debut.strftime("%H:%M")
		print(date_debut_evenement)
		


		date_fin = dt.datetime.strptime(date_fin_str, '%Y-%m-%dT%H:%M')
		print("date_debut", date_debut)
		print("date_fin", date_fin)
		nom_patient = request.POST.get('nom')
		if date_debut > date_fin:
			messages.error(request, "Date de debut ou de fin erroné")
			return render(request, 'ajouter-rdv.html', context)

		dates_de_debut = Rdv.objects.filter(date_rdv =date_debut)
		print("**********************************",dates_de_debut)
		for d in dates_de_debut:
			if d.date_rdv == date_debut:
				print( d.date_rdv)
				messages.error(request, "Vous avez déja créé un rdv dont la date de debut et la meme. supprimer le ou bien changer de date")
				return render(request, 'ajouter-rdv.html', context)


		form = RdvForm(request.POST or None)
		if form.is_valid():
			print("form is valid")
			rdv = form.save()
			print(rdv.id)
			evenement = Event(title = ''+nom_patient+' : '+date_debut_evenement+'',start_time=date_debut,end_time=date_fin, rdv=rdv )
			print("evenement = ",evenement.title)
			evenement.save()
			messages.success(request, 'Rendez-vous a été bien ajouté')
			return render(request, 'ajouter-rdv.html', context)
		else:
			print("form n'est pas valide")
			messages.error(request, form_validation_error(form))
	return render(request, 'ajouter-rdv.html', context)

@login_required(login_url="/login/")
def liste_rdv(request):
	context = {}
	context['segment'] = 'rdvs'
	
	rdv = Rdv.objects.values().order_by('updated_at')
	print(rdv)
	context['rdv_list'] = rdv
	return render(request, "liste-rdv.html", context)
@login_required(login_url="/login/")	
def confirmer_rdv(request):
	context = {}
	context['segment'] = 'rdvs'
	if request.method =="POST":
		idRdv = request.POST.get('id')
		Rdv.objects.filter(id=idRdv).update(statut='confirmer')

	rdv=Rdv.objects.values().order_by('updated_at')
	context['rdv_list']=rdv
	return render(request, "liste-rdv.html", context)
@login_required(login_url="/login/")
def ajouter_patient_from_rdv(request):
	context = {}
	if request.method== "POST":
		nom_patient = request.POST.get('nom')
		print(nom_patient)

		prenom_patient = request.POST.get('prenom')
		print(prenom_patient)
		patients = Patient.objects.filter(nom=nom_patient).filter(prenom = prenom_patient)
		print("**********", patients)
		if patients:
			messages.warning(request, "Il exite déja un patient avec le méme nom et prenom")
			context['patient_list'] = Patient.objects.filter(nom=nom_patient).filter(prenom = prenom_patient)
			return render(request, "liste-patient.html", context)

	context = {

	     "nom" : nom_patient,
	     "prenom":prenom_patient,
	}

	return render(request, 'ajouter-patient.html', context)
@login_required(login_url="/login/")
def supprimer_rdv(request):
	context = {}
	if request.method =="POST":
		id_rdv = request.POST.get('id')
		print(id_rdv)
		rdv1 = Rdv.objects.get(id = id_rdv)
		rdv1.delete()
	rdvs = Rdv.objects.values().order_by('updated_at').reverse()
	
	context['rdv_list'] = rdvs
	return render(request, "liste-rdv.html", context)

@login_required(login_url="/login/")
def list_rdv_toDay(request):
	context = {}
	context['segment'] = 'list_rdv_toDay'
	today = datetime.today()
	rdvs = Rdv.objects.filter(statut="confirmer").filter(date_rdv__year=today.year, date_rdv__month=today.month, date_rdv__day=today.day).order_by('date_rdv')
	context['rdv_list'] = rdvs


	return render(request, "dashboard.html", context)

@login_required(login_url="/login/")
def list_rdv_week(request):
	context = {}
	context['segment'] = 'list_rdv_week'
	date = dt.date.today()
	start_week = date - dt.timedelta(date.weekday()+1)
	end_week = start_week + dt.timedelta(7)
	rdvs = Rdv.objects.filter(statut="confirmer").filter(date_rdv__date__range=[start_week, end_week])

	context['rdv_list'] = rdvs
	context['par_'] = 'semaine'
    
	return render(request, "dashboard.html", context)

@login_required(login_url="/login/")
def list_rdv_month(request):
	context = {}
	context['segment'] = 'list_rdv_month'
	rdvs = Rdv.objects.filter(statut="confirmer").filter(date_rdv__gte=datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0))
	context['rdv_list'] = rdvs
	print(rdvs)
	context['par_'] = 'mois'

	return render(request, "dashboard.html", context)

@login_required(login_url="/login/")
def ajouter_rdv_formulaire(request):
	context = {}
	nom = ""
	prenom = ""
	if request.method =="POST":
		nom = request.POST.get('nom')
		prenom = request.POST.get('prenom')

	context['nom'] = nom 
	context['prenom'] = prenom
	context['segment'] = 'list_rdv_week'
	context['typrrdv_list'] = Typerdv.objects.all()
	return render(request, "ajouter-rdv.html", context)


@login_required(login_url="/login/")
def modifier_rdv(request, event_id=None):
	context = {}
	instance = Event()
	if event_id:
		instance = get_object_or_404(Event, pk=event_id)
	else:
		instance = Event()

	print("instance",instance.id)

	event = Event.objects.get(id=instance.id)
	rdv_objet = event.rdv
	print(rdv_objet)
	context['typrrdv_list'] = Typerdv.objects.all()
	context['rdv'] = rdv_objet
	return render(request, "modifier_rdv.html", context)


@login_required(login_url="/login/")
def modifier_rdv_from_planning (request):
	context = {}
	if request.method =="POST":
		id_rdv = request.POST.get('id')
		nom = request.POST.get('nom')
		prenom = request.POST.get('prenom')
		type_rdv = request.POST.get('type_rdv')
		date_rdv = request.POST.get('date_rdv')
		date_fin = request.POST.get('date_fin')
	Rdv.objects.filter(id=id_rdv).update(nom=nom)
	Rdv.objects.filter(id=id_rdv).update(prenom=prenom)
	Rdv.objects.filter(id=id_rdv).update(type_rdv=type_rdv)
	if(date_rdv):
		Rdv.objects.filter(id=id_rdv).update(date_rdv=dt.datetime.strptime(date_rdv, '%Y-%m-%dT%H:%M'))
	if(date_fin):
		Rdv.objects.filter(id=id_rdv).update(date_fin= dt.datetime.strptime(date_fin, '%Y-%m-%dT%H:%M'))

	date_debut_evenement = Rdv.objects.get(id=id_rdv).date_rdv
	date_fin_evenement = Rdv.objects.get(id=id_rdv).date_fin

	date_debut_evenement_str = Rdv.objects.get(id=id_rdv).date_rdv.strftime("%H:%M")

	Event.objects.filter(rdv=Rdv.objects.get(id=id_rdv))
	Event.objects.filter(rdv=Rdv.objects.get(id=id_rdv)).update(title =''+nom+' : '+date_debut_evenement_str+'')
	Event.objects.filter(rdv=Rdv.objects.get(id=id_rdv)).update(start_time= date_debut_evenement)
	Event.objects.filter(rdv=Rdv.objects.get(id=id_rdv)).update(end_time =date_fin_evenement)
	

	
	url = reverse('cal:calendar')
	return  HttpResponseRedirect(url)





















