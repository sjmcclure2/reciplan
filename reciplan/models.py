#File:       models.py
#Authors:    Joshua Coe, Scott McClure, Danita Hodges
#Purpose:    Define models for ReciPlan app
##Version:   1.2
#Version Notes:
#            1.0 - JC - Initial creation, initial model creation
#            1.1 - SM - Ingredients model
#            1.2 - DH - Added title string for recipe model
#            1.3 - DH - Fixed object title formatting, added directions
#                       model. Added verbose names to recipe and
#                       ingredient models. Set URL source to nullable   
#test

from ensurepip import version
from django.db import models
from . import conversions
from django.urls import reverse

class Recipe(models.Model):

    def __str__(self):
        return '{} - {}'.format(self.pk, self.title)

    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    o_yield = models.IntegerField(verbose_name="Yield (servings)")
    #directions = models.TextField()
    image = models.ImageField(upload_to="reciplan/images/", blank=True)
    url = models.URLField(blank=True, verbose_name="URL Source", null=True)

class Ingredients(models.Model):
    
    def __str__(self):
        return '{} / {}'.format(self.name, self.recipe)
    
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    name = models.CharField(max_length = 50, verbose_name="Item")
    amt = models.FloatField(verbose_name="Amount")
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
    unit_of_measure = models.CharField(max_length=100, choices = UOM, verbose_name="Unit of Measure")
    cup_amt = models.FloatField(null=True)

class Direction(models.Model):
    def __str__(self):
        return '{} - Step {}'.format(self.recipe, self.step)

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    step = models.IntegerField(null=True)
    instruction = models.CharField(max_length = 200, null=True)