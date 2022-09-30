from django.db import models


# Create your models here.

class bitcoin_price(models.Model):
    Symbol = models.CharField(max_length=30)
    price = models.FloatField()
    time = models.DateTimeField()

class bitcoin(models.Model):
    Symbol = models.CharField(max_length=30)
    price = models.IntegerField()
    time = models.DateTimeField()



