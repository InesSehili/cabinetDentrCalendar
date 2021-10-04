from django.db import models
from patients.models import Patient
from django.core.validators import MinValueValidator
from decimal import Decimal

# Create your models here.*
class Radio(models.Model):
	patient =  models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True)
	titre_radio = models.CharField(max_length=55)
	observation = models.TextField(blank=True, null=True)
	radio_pdf = models.FileField(upload_to='radios/%Y/%m/%d/')
	prix_radio = models.DecimalField(decimal_places=2, max_digits=65, blank=True, null=True, default=0, validators=[MinValueValidator(Decimal('0.01'))])
	prix_paye = models.DecimalField(decimal_places=2, max_digits=65, blank=True, null=True, default=0)
	reste = models.DecimalField(decimal_places=2, max_digits=65, blank=True, null=True, default=0)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)






