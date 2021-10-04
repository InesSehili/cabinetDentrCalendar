from django.shortcuts import render, redirect
from achats.forms import AchatForm, form_validation_error
from achats.models import Achat
from django.contrib import messages
from fournisseurs.models import Fournisseur
from depenses.models import Depense
import decimal
from django.contrib.auth.decorators import login_required
from core.decorators import allowed_users
from django.http import FileResponse
import io 
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch 
from reportlab.lib.pagesizes import letter

# Create your views here.
@login_required(login_url="/login/")
@allowed_users(allowed_roles=['dentiste'])
def ajouter_achat(request):
	context = {}
	if request.method == "POST":
		fournisseur = request.POST.get('fournisseur')
		print("Fournisseur",fournisseur)
		matiere = request.POST.get('matiere')
		print(matiere)
		prix = request.POST.get('prix')
		print(prix)
		prix_payer = request.POST.get('prix_payer')
		print(prix_payer)
		context['fournisseur'] = fournisseur
		context['nom_fournisseur'] = Fournisseur.objects.get(id=fournisseur).raison_social
		# if int(prix_payer) > int(prix) :
		# 	messages.error(request, 'Prix erroné')
		# 	return render(request, 'ajouter-achat.html', context)


		rest = int(prix) - int(prix_payer)
		f = Fournisseur.objects.get(id=fournisseur)
		form = AchatForm(request.POST or None)

		if form.is_valid():
			print("form is valid")
			achat = form.save()
			

			
			messages.success(request, 'Achat a été bien crée')
			context['fournisseur'] = fournisseur
			context['nom_fournisseur'] = Fournisseur.objects.get(id=fournisseur).raison_social
			context['list_achat'] = Achat.objects.filter(fournisseur=fournisseur)
			return render(request, 'ajouter-achat.html', context)
		else:
			messages.error(request, "le prix d'achat doit étre superieur ou égal a 0")
			context['fournisseur'] = fournisseur
			context['nom_fournisseur'] = Fournisseur.objects.get(id=fournisseur).raison_social
			context['list_achat'] = Achat.objects.filter(fournisseur=fournisseur)
			return render(request, 'ajouter-achat.html', context)
	return render(request, 'ajouter-achat.html', context)

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['dentiste'])
def fourmulaire_ajout_achat(request):
	context = {}
	if request.method == "POST":
		fournisseur = request.POST.get('fournisseur')


	context['fournisseur'] = fournisseur
	context['nom_fournisseur'] = Fournisseur.objects.get(id=fournisseur).raison_social
	print(context['nom_fournisseur'])
	context['list_achat'] = Achat.objects.filter(fournisseur=fournisseur)

	return render(request, 'ajouter-achat.html', context)

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['dentiste'])
def formulaire_payer_achat(request):
	context = {}
	if request.method == "POST":
		fournisseur = request.POST.get('fournisseur')
		print(fournisseur)
		achat = request.POST.get('achat')
		print(achat)

		achat_obj = Achat.objects.get(id = achat) 
		context['achat'] = achat_obj
	return render(request, 'payer-achat.html', context)

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['dentiste'])
def payer_achat(request):
	context = {}
	if request.method == "POST":
		fournisseur = request.POST.get('fournisseur')
		print('fournisseur =' , fournisseur)
		achat = request.POST.get('achat')
		print('achat', achat)
		prix_payer = request.POST.get('prix_payer')
		print('prix payé', prix_payer)
		reste = request.POST.get('reste')
		print(" reste",reste)
		context['fournisseur'] = fournisseur
		context['nom_fournisseur'] = Fournisseur.objects.get(id=fournisseur).raison_social
		if decimal.Decimal(prix_payer)> decimal.Decimal(reste) or decimal.Decimal(prix_payer)<0 :
			messages.error(request, 'Prix payé erroné')
			
			
			achat_obj = Achat.objects.get(id = achat) 
			context['achat'] = achat_obj
			return render(request, 'payer-achat.html', context)
		prix_payer_premier = Achat.objects.get(id=achat).prix_payer
		Achat.objects.filter(id=achat).update(prix_payer=prix_payer_premier+ decimal.Decimal(prix_payer))
		Achat.objects.filter(id=achat).update(reste=decimal.Decimal(reste)- decimal.Decimal(prix_payer))
		premier_reste_paye = Fournisseur.objects.get(id=fournisseur).reste_paye
		premier_payer = Fournisseur.objects.get(id=fournisseur).prix_paye
		Fournisseur.objects.filter(id=fournisseur).update(reste_paye=premier_reste_paye-decimal.Decimal(prix_payer))
		Fournisseur.objects.filter(id=fournisseur).update(prix_paye=premier_payer+decimal.Decimal(prix_payer))
		nom_fournisseur = Fournisseur.objects.get(id = fournisseur ).raison_social
		messages.success(request, "l'achat a été payé avec succées")
		depense = Depense(prix_sortie=decimal.Decimal(prix_payer),raison_payement='fournisseur', id_raison = fournisseur, id_achat =achat, fournisseur=nom_fournisseur )
		depense.save()
		context['list_achat'] = Achat.objects.filter(fournisseur=fournisseur)
		return render(request, 'ajouter-achat.html', context)

	return render(request, 'ajouter-achat.html', context)

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['dentiste'])
def supprimer_achat(request):
	context = {}
	if request.method == "POST":
		id_achat = request.POST.get("achat")
		id_fournisseur = request.POST.get("fournisseur")
		prix_achat = request.POST.get("prix_achat")
		prix_payer = request.POST.get("prix_payer")
		etat =  request.POST.get("etat")
	if etat == "Valide":
		prix_payer_achat = Achat.objects.get(id =id_achat).prix_payer
		prix_total_fournissuer = Fournisseur.objects.get(id=id_fournisseur).total_payement
		Fournisseur.objects.filter(id=id_fournisseur).update(total_payement=prix_total_fournissuer-decimal.Decimal(prix_achat))
		fournisseur_prix_paye = Fournisseur.objects.get(id=id_fournisseur).prix_paye
		Fournisseur.objects.filter(id=id_fournisseur).update(prix_paye=fournisseur_prix_paye - prix_payer_achat)
		prix_total_fournissuer = Fournisseur.objects.get(id=id_fournisseur).total_payement
		fournisseur_prix_paye = Fournisseur.objects.get(id=id_fournisseur).prix_paye
		retse = prix_total_fournissuer - fournisseur_prix_paye
		Fournisseur.objects.filter(id=id_fournisseur).update(reste_paye=retse)
	
	
	
	achat = Achat.objects.get(id = id_achat)
	nv_payement = achat.prix_payer
	achat.delete()
	if nv_payement != 0:
		Depense.objects.filter(id_achat=id_achat).delete()
		


	
	
	context['list_achat'] = Achat.objects.filter(fournisseur=id_fournisseur)
	context['nom_fournisseur'] = Fournisseur.objects.get(id=id_fournisseur).raison_social
	context['fournisseur'] = id_fournisseur
	return render(request, 'ajouter-achat.html', context)
@login_required(login_url="/login/")
@allowed_users(allowed_roles=['dentiste'])



@login_required(login_url="/login/")
@allowed_users(allowed_roles=['dentiste'])
def imprimer_bon_commande(request):
	buf = io.BytesIO()
	c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
	textob = c.beginText()
	textob.setTextOrigin(inch, inch)
	textob.setFont("Helvetica", 14)
	lines = [
	  "Date:",
	  "Nom patient:",
	  "Prenom patient:",
	  "Nom medecin:",


	]
	for line in lines:
		textob.textLine(line)
		c.drawText(textob)
		c.showPage()
		c.save()
		buf.seek(0)
		return FileResponse(buf, as_attachment=True, filename='fchier.pdf')


	






@login_required(login_url="/login/")
@allowed_users(allowed_roles=['dentiste'])
def valider_bon_commande(request):
	context = {}
	if request.method == "POST":
		fournisseur = request.POST.get('fournisseur')
		print(fournisseur)
		last_achat = request.POST.get('achat')
		print(last_achat)
		prix = request.POST.get('prix_achat')
		print(prix)
		prix_payer = request.POST.get('prix_payer')
		print(prix_payer)

	rest = decimal.Decimal(prix) - decimal.Decimal(prix_payer)
	Achat.objects.filter(id=last_achat).update(etat="Valide")


	Achat.objects.filter(id=last_achat).update(reste=rest)
	prix_total_fournissuer = Fournisseur.objects.get(id=fournisseur).total_payement
	prix_payer_fournissuer = Fournisseur.objects.get(id=fournisseur).prix_paye
	prix_reste_fournissuer = Fournisseur.objects.get(id=fournisseur).reste_paye
	Fournisseur.objects.filter(id=fournisseur).update(total_payement=prix_total_fournissuer+decimal.Decimal(prix))
	Fournisseur.objects.filter(id=fournisseur).update(prix_paye=prix_payer_fournissuer+decimal.Decimal(prix_payer))
	Fournisseur.objects.filter(id=fournisseur).update(reste_paye=prix_reste_fournissuer+decimal.Decimal(rest))
	messages.success(request, 'Vous avez valider votre commande')
	context['fournisseur'] = fournisseur
	context['nom_fournisseur'] = Fournisseur.objects.get(id=fournisseur).raison_social
	context['list_achat'] = Achat.objects.filter(fournisseur=fournisseur)
	return render(request, 'ajouter-achat.html', context)























	















