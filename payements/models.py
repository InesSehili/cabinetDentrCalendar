from django.db import models
from patients.models import Patient
from django.core.validators import MinValueValidator
from decimal import Decimal

# Create your models here.
class Payement(models.Model):
	patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True)
	prix_payer = models.DecimalField(decimal_places=2, max_digits=65, blank=True, default=0, validators=[MinValueValidator(Decimal('0.01'))])
	payement_de =  models.CharField(max_length=32, null=True, blank=True)
	user = models.CharField(max_length=32, null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	
