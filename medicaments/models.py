from django.db import models

# Create your models here.
class Medicament(models.Model):
	nom_medicament = models.CharField(max_length=100, null=True, blank=True)
	dose = models.CharField(max_length=100, null=True, blank=True)
	forme = models.CharField(max_length=100, null=True, blank=True)
	updated_at = models.DateTimeField(auto_now=True)
	


	