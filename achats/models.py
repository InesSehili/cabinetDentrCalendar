from django.db import models
from fournisseurs.models import Fournisseur
from django.core.validators import MinValueValidator
from decimal import Decimal

# Create your models here.
class Achat(models.Model):
	fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE, null=True, blank=True)
	matiere = models.CharField(max_length=32, null=True, blank=True)
	prix =  models.DecimalField(decimal_places=2, max_digits=65, blank=True, default=0, validators=[MinValueValidator(Decimal('0.01'))])
	prix_payer = models.DecimalField(decimal_places=2, max_digits=65, blank=True, default=0)
	reste =  models.DecimalField(decimal_places=2, max_digits=65, blank=True, default=0)
	etat = models.CharField(max_length=32, blank=True, default="En cours")

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)



