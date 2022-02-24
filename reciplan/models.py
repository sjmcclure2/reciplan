#File:       models.py
#Authors:    Joshua Coe, Scott McClure, Danita Hodges
#Purpose:    Define models for ReciPlan app
##Version:   1.2
#Version Notes:
#            1.0 - JC - Initial creation, initial model creation
#            1.1 - SM - Ingredients model
#            1.2 - DH - Added title string for recipe model

from django.db import models
from . import conversions
from django.urls import reverse

class Recipe(models.Model):

    def __str__(self):
        return self.title

    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    o_yield = models.IntegerField()
    directions = models.TextField()
    image = models.ImageField(upload_to="reciplan/images/", blank=True)
    url = models.URLField(blank=True)

class Ingredients(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    name = models.CharField(max_length = 50)
    amt = models.FloatField()
    UOM = (
        ('fl_oz', 'fl_oz'),
        ('fl_cups', 'fl_cups'),
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