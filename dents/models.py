from django.db import models

# Create your models here.
class Dent(models.Model):
	num_dent = models.CharField(max_length=100, blank=True, null=True)