from django.db import models

# Create your models here.
class Patient(models.Model):

	nom = models.CharField(max_length=100)
	prenom = models.CharField(max_length=100)
	date_naissance = models.DateField(null=True, blank=True)
	sexe = models.CharField(max_length=32, null=True, blank=True)
	adresse = models.CharField(max_length=255, null=True, blank=True)
	numero_tel = models.CharField(max_length=32, null=True, blank=True)
	email = models.EmailField(max_length=254,null=True, blank=True)
	ville = models.CharField(max_length=50, null=True, blank=True)
	archiver = models.BooleanField(default=False, null=True, blank=True)
	fiche_medical = models.BooleanField(default=True, blank=True,  null=True)
	profession = models.CharField(max_length=100, null=True, blank=True)
	prix_paye = models.DecimalField(default=0, decimal_places=2, max_digits=65, blank=True, null=True)
	reste_paye = models.DecimalField(default=0, decimal_places=2, max_digits=65, blank=True, null=True) 
	total_payement = models.DecimalField(default=0,decimal_places=2, max_digits=65, blank=True, null=True) 
	estimation_du_coût_de_traitement = models.DecimalField(default=0, decimal_places=2, max_digits=65, blank=True, null=True) 
	radio_existe =  models.BooleanField(default=False, null=True, blank=True)
	consultation_existe = models.BooleanField(default=False, null=True, blank=True)
	fiche_medical_existe = models.BooleanField(default=False, null=True, blank=True)



	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


   
