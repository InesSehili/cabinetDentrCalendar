from django.db import models
from patients.models import Patient
from django.core.validators import MinValueValidator
from decimal import Decimal

# Create your models here.
class Consultation(models.Model):
	patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True)
	prix_defini = models.DecimalField(decimal_places=2, max_digits=65, blank=True, default=0, validators=[MinValueValidator(Decimal('0.01'))])
	prix_paye = models.DecimalField(decimal_places=2, max_digits=65, blank=True, default=0)
	reste = models.DecimalField(decimal_places =2, max_digits=65, blank=True, default=0)

	diagnostique_existe =  models.BooleanField(default=False, null=True, blank=True)
	traitement_existe =  models.BooleanField(default=False, null=True, blank=True)
	ordonance_existe = models.BooleanField(default=False, null=True, blank=True)

	etat_payement = models.CharField(max_length=32, null=True, blank=True, default='non_payer')
	estimation_du_coût_de_traitement = models.DecimalField(default=0, decimal_places=2, max_digits=65, blank=True, null=True)



	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
