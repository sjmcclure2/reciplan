from django.db import models
from . import conversions

class Recipe(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    o_yield = models.IntegerField()
    directions = models.TextField()
    image = models.ImageField(upload_to="reciplan/images/", blank=True)
    url = models.URLField(blank=True)

class Ingredients(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    name = models.CharField(max_length = 50)
    amt = models.IntegerField()
    UOM = (
        ('fl_oz', 'fl oz'),
        ('fl_cups', 'fl cups'),
        ('cups', 'cups'),
        ('pints', 'pints'),
        ('quarts', 'quarts'), 
        ('gallons', 'gallons'), 
        ('tsp', 'tsp'), 
        ('Tbsp', 'Tbsp'),
        ('grams', 'grams'),
        ('Kg', 'Kg'),
        ('oz', 'oz'),
        ('lbs', 'lbs'),
        ('mL', 'mL'),
        ('liters', 'liters'),
        ('ea', 'ea')
    )
    unit_of_measure = models.CharField(max_length=100, choices = UOM)
    cup_amt = models.FloatField(null=True)
    
  
