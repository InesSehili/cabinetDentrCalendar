from django.shortcuts import render, redirect
from ordonances.forms import OrdonanceForm, form_validation_error
from django.contrib import messages
from medicaments.models import Medicament
import json
from django.core.serializers.json import DjangoJSONEncoder
from ordonances.models import Ordonance
from consultations.models import Consultation
from django.utils import timezone
from django.http import FileResponse
import io 
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch 
from reportlab.lib.pagesizes import letter
from quantites.models import Quantite
from django.contrib.auth.decorators import login_required
from core.decorators import allowed_users
from PyPDF2 import PdfFileWriter, PdfFileReader


# Create your views here.
@login_required(login_url="/login/")
@allowed_users(allowed_roles=['dentiste'])
def view_pdf(request):
	#create Bytestream buffer
	buf = io.BytesIO()
	#create a canvas
	c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
	#Create a text object
	textob = c.beginText()
	textob.setTextOrigin(inch, inch)
	textob.setFont("Helvetica", 14)
	#add some lines of text
	if request.method =="POST":
		id_ordonance = request.POST.get('id')
		date = request.POST.get('date')

	ordonance = Ordonance.objects.get(consultation=id_ordonance)
	age = ordonance.age
	nom = ordonance.consultation.patient.nom
	prenom = ordonance.consultation.patient.prenom
	ville= "Constantine"
	
	new_date = date.split()[0]+date.split()[1]+date.split()[2]

	quantite = Quantite.objects.all().filter(ordonance=id_ordonance)
	lines = ["",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",]
	#loop
    
	for q in quantite:
		lines.append('- '+ q.medicament.nom_medicament +','+ q.medicament.dose+','+ q.medicament.forme+ ',              qte = '+ q.quantite+'boite.')
		lines.append('')

	for line in lines:
		textob.textLine(line)
	#Finish Up
	c.drawText(textob)
	c.drawString(510, 205,  age)
	c.drawString(61, 205, nom)
	c.drawString(289, 205, prenom)
	c.drawString(273, 175, ville)
	c.drawString(489, 175,new_date)
	c.showPage()
	c.save()
	buf.seek(0)
	new_pdf = PdfFileReader(buf)
	existing_pdf = PdfFileReader(open("ordonancelogiciel.pdf", "rb"))
	output = PdfFileWriter()
	page = existing_pdf.getPage(0)
	page.mergePage(new_pdf.getPage(0))
	output.addPage(page)
	outputStream = open("destination.pdf", "wb")
	output.write(outputStream)
	outputStream.close()

	#Return something
	return FileResponse(open("destination.pdf", 'rb'), content_type='application/pdf')
@login_required(login_url="/login/")
@allowed_users(allowed_roles=['dentiste'])
def formulaire_creation_ordonance(request):
	context = {}
	context['segment'] = 'ordonances'
	if request.method =="POST":
		id_consultation = request.POST.get('id')
		print('id' + id_consultation)
		nom_patient = request.POST.get('nom')
		print('nom ' + nom_patient)
		prenom_patient = request.POST.get('prenom')
		print('prenom ' + prenom_patient)



	context['id'] = id_consultation
	context['nom'] = nom_patient
	context['prenom'] = prenom_patient
	
	context['medicament_list'] =  list(Medicament.objects.all().values().order_by('updated_at'))
	l = list(Medicament.objects.all().values().order_by('updated_at'))
	medicament_json = json.dumps(list(l), cls=DjangoJSONEncoder)
	context['medicament']= medicament_json


	return render(request, "ajouter-ordonance.html", context)
@login_required(login_url="/login/")
@allowed_users(allowed_roles=['dentiste'])
def ajouter_ordonance(request):
	context = {}
	context['segment'] = 'ordonances'
	if request.method == "POST":
		id_consultation = request.POST.get('id')
		print('id_consultation'+id_consultation)
		nom_patient = request.POST.get('nom')
		print('nom_patient'+nom_patient)
		prenom_patient = request.POST.get('prenom')
		print('prenom_patient'+prenom_patient)
		age_patient = request.POST.get('age')
		print('age_patient'+age_patient)
		nom_medecin = request.POST.get('medecin')
		print('nom_medecin'+nom_medecin)
		medicament = request.POST.getlist('medicament_options[]')
		print(medicament)
		quantite = request.POST.getlist('quantite_options[]')
		print(quantite)
	# a1 = Article(headline='Django lets you build Web apps easily')
	c = Consultation.objects.get(id=id_consultation)
	o1 = Ordonance(consultation=c, age=age_patient, nom_medecin=nom_medecin, created_at=timezone.now())
	o1.save()
	Consultation.objects.filter(id=id_consultation).update(ordonance_existe=True)
	messages.success(request, 'Ordonance a été bien crée')

	print("nb medicament =", len(medicament))


	for i in range(len(medicament)):

		obj_medicament = Medicament.objects.get(id=medicament[i])
		obj_quantite = Quantite(ordonance=o1, medicament= obj_medicament, quantite= quantite[i])

		result = obj_quantite.save() 
		print(result)
		if(True):
			o1.medicaments.add((obj_medicament))
			
	
		

	context['ordonance_list'] = Ordonance.objects.all().order_by('created_at')
	return render(request, "liste-ordonance.html", context)
@login_required(login_url="/login/")
@allowed_users(allowed_roles=['dentiste'])
def list_medicament_ordonance(request):
	context = {}
	context['segment'] = 'ordonances'
	if request.method =="POST":
		id_ordonance = request.POST.get('id')
	print("id ="+ id_ordonance )

	ordonance = Ordonance.objects.get(consultation=id_ordonance)

	quantite = Quantite.objects.all().filter(ordonance=id_ordonance)

	print(quantite.count())
	context['quantite'] = quantite
	context['id'] = id_ordonance


	return render (request, 'liste-medicament-ordonance.html', context)


@login_required(login_url="/login/")
@allowed_users(allowed_roles=['dentiste'])
def liste_ordonance(request):
	context = {}
	context['segment'] = 'ordonances'
	context['ordonance_list'] = Ordonance.objects.all().order_by('created_at').reverse()
	return render(request, "liste-ordonance.html", context)
@login_required(login_url="/login/")
@allowed_users(allowed_roles=['dentiste'])
def supprimer_ordonance(request):
	context = {}
	if request.method=="POST":
		id_ordonance = request.POST.get('id')
		ordonance = Ordonance.objects.get(consultation = id_ordonance)
		ordonance.delete()
		Consultation.objects.filter(id=id_ordonance).update(ordonance_existe=False)
		context['ordonance_list'] = Ordonance.objects.all().order_by('created_at')
		return render(request, "liste-ordonance.html", context)


# def gerer_ordonance(request):
# 	context = {}
# 	packet = io.BytesIO()
# 	# create a new PDF with Reportlab
# 	can = canvas.Canvas(packet, pagesize=letter)
# 	can.drawString(10, 100, "Hello world")
# 	can.save()
# 	#move to the beginning of the StringIO buffer
# 	packet.seek(0)
# 	new_pdf = PdfFileReader(packet)
# 	# read your existing PDF
# 	existing_pdf = PdfFileReader(open("original.pdf", "rb"))
# 	output = PdfFileWriter()
# 	# add the "watermark" (which is the new pdf) on the existing page
# 	page = existing_pdf.getPage(0)
# 	page.mergePage(new_pdf.getPage(0))
# 	output.addPage(page)
# 	# finally, write "output" to a real file
# 	outputStream = open("destination.pdf", "wb")
# 	output.write(outputStream)   
# 	outputStream.close()




  





	



