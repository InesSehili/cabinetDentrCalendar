from django.db import models
from ordonances.models import Ordonance
from medicaments.models import Medicament

# Create your models here.
class Quantite(models.Model):
	ordonance = models.ForeignKey(Ordonance, on_delete=models.CASCADE, null=True, blank=True)
	medicament = models.ForeignKey(Medicament, on_delete=models.CASCADE, null=True, blank=True)
	quantite = models.CharField(max_length = 100, null=True, blank=True)
