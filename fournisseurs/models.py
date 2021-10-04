from django.db import models

# Create your models here.
class Fournisseur(models.Model):
	raison_social = models.CharField(max_length=100, null=True, blank=True)
	num_tel = models.CharField(max_length=32, null=True, blank=True, unique=True)
	email = models.EmailField(max_length=254,null=True, blank=True)
	nif =  models.CharField(max_length=100, null=True, blank=True)
	nis =  models.CharField(max_length=100, null=True, blank=True)
	rc =  models.CharField(max_length=100, null=True, blank=True)

	prix_paye = models.DecimalField(default=0, decimal_places=2, max_digits=65, blank=True, null=True)
	reste_paye = models.DecimalField(default=0, decimal_places=2, max_digits=65, blank=True, null=True) 
	total_payement = models.DecimalField(default=0,decimal_places=2, max_digits=65, blank=True, null=True) 

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

