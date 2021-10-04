from django.db import models

# Create your models here.
class Employee(models.Model):
	nom = models.CharField(max_length=100, null=True, blank=True)
	prenom = models.CharField(max_length=100, null=True, blank=True)
	num_tel = models.CharField(max_length=32, null=True, blank=True, unique=True)
	salary = models.DecimalField(default=0, decimal_places=2, max_digits=65, blank=True, null=True)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	

