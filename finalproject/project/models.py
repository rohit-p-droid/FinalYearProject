from django.db import models

# Create your models here.
class Monuments(models.Model):
    city = models.CharField(max_length=122)
    monument = models.CharField(max_length=122)
    indPrice = models.CharField(max_length=10)
    foreignPrice = models.CharField(max_length=10)
    
class Ticket(models.Model):
    id = models.CharField(max_length=20, primary_key=True, auto_created=True)
    city = models.CharField(max_length=122)
    monument = models.CharField(max_length=122)
    ticketCount = models.IntegerField()
    ticketPrice = models.CharField(max_length=10)
    totalPrice = models.CharField(max_length=10)
    time = models.CharField(max_length=20)
    date = models.DateField()
    transactionId = models.CharField(max_length=20, auto_created=True, unique=True)
    email = models.CharField(max_length=122, default="admin@gmail.com")
    scanned = models.BooleanField(default=False)