from django.db import models

# Create your models here.
class Rdv(models.Model):
    nom = models.CharField(max_length = 100)
    prenom = models.CharField(max_length = 100)
    type_rdv = models.CharField(max_length = 100, null=True, blank=True)
    date_rdv = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    date_fin = models.DateTimeField(auto_now=False, auto_now_add=False)
    statut = models.CharField(max_length=50, default='en cours', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)


	
