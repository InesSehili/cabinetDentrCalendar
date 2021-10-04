from django.db import models

# Create your models here.
class Typerdv(models.Model):
	nom_typerdv = models.CharField(max_length=50, null=True, blank=True)
	description = models.TextField(blank=True, null=True)
