from django.db import models
from consultations.models import Consultation

# Create your models here.
class Diagnostique(models.Model):
	consultation = models.OneToOneField(Consultation, on_delete=models.CASCADE, primary_key=True)
	txt_diagnostique = models.CharField(max_length=100, null=True, blank=True)
	nom_medecin =  models.CharField(max_length=50, null=True, blank=True)
	observation = models.TextField(blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)


