from tkinter import CASCADE
from django.db import models
from sqlalchemy import ForeignKey

# Create your models here.
class Recipe(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    image = models.ImageField(upload_to="reciplan/images/")
    url = models.URLField(blank=True)


class Ingredients(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=CASCADE)
    name = models.CharField(max_length=50)
    amt = models.IntegerField()
    unit_of_measure = models.CharField(max_length=10)
