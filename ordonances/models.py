from django.db import models
from django.contrib import messages
from medicaments.models import Medicament
from consultations.models import Consultation

# Create your models here.
class Ordonance(models.Model):
	consultation = models.OneToOneField(Consultation, on_delete=models.CASCADE, primary_key=True)
	created_at = models.DateTimeField(auto_now_add=True)
	age = models.CharField(max_length=50, null=True, blank=True)
	nom_medecin = models.CharField(max_length=50, null=True, blank=True)
	medicaments = models.ManyToManyField(Medicament)


