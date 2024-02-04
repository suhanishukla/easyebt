from django.db import models

# Create your models here.
class GroceryList(models.Model): 
    type=models.CharField(max_length=255)
    name=models.CharField(max_length=255)
    price=models.CharField(max_length=255)
    rating=models.CharField(max_length=255)
    inlist=models.BooleanField(default=True)
    
