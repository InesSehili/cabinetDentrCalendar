from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

# Create your models here.
class Depense(models.Model):
	prix_sortie = models.DecimalField(decimal_places=2, max_digits=65, blank=True, default=0, validators=[MinValueValidator(Decimal('0.01'))])
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	raison_payement =  models.CharField(max_length=32, null=True, blank=True)
	note = models.TextField(blank=True, null=True)
	employee =  models.CharField(max_length=32, null=True, blank=True, default='/')
	fournisseur = models.CharField(max_length=32, null=True, blank=True, default='/') 
	id_raison = models.DecimalField(decimal_places=0, max_digits=65, blank=True, default=0)
	id_achat = models.DecimalField(decimal_places=0, max_digits=65, blank=True, default=0)
