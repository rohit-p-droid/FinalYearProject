from django.db import models

# Create your models here.
class Monuments(models.Model):
    city = models.CharField(max_length=122)
    monument = models.CharField(max_length=122)
    indPrice = models.CharField(max_length=10)
    foreignPrice = models.CharField(max_length=10)
    
