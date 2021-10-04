from django.db import models
from consultations.models import Consultation
from dents.models import Dent
from django.core.validators import MinValueValidator
from decimal import Decimal

# Create your models here.
class Traitement(models.Model):
	consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE, null=True, blank=True)
	dent = models.ForeignKey(Dent, on_delete=models.CASCADE, null=True, blank=True)
	traitement = models.CharField(max_length=100, null=True, blank=True)
	description_traitement = models.TextField(blank=True, null=True)
	prix_traitement = models.DecimalField(decimal_places=2, max_digits=65, blank=True, default=0, validators=[MinValueValidator(Decimal('0.01'))])
	reste_traitement = models.DecimalField(decimal_places=2, max_digits=65, blank=True, default=0)
	prix_payer_traitement = models.DecimalField(decimal_places=2, max_digits=65, blank=True, default=0)
	etat_traitement = models.CharField(max_length=32, null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


