from django.db import models
from patients.models import Patient

# Create your models here.
class FicheMedical(models.Model):
	patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True)
	groupage = models.CharField(max_length=32, null=True, blank=True)
	antecF = models.CharField(max_length=32, null=True, blank=True)
	antecC = models.CharField(max_length=32, null=True, blank=True)
	antecM = models.CharField(max_length=32, null=True, blank=True)
	antecA= models.CharField(max_length=32, null=True, blank=True)
	maladie_axcecie = models.CharField(max_length=100, null=True, blank=True)
	medication_encours = models.CharField(max_length=100, null=True, blank=True)
	histoire_de_la_maladie = models.TextField(blank=True, null=True)
	