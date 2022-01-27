from django.db import models

class Recipe(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    o_yield = models.IntegerField()
    directions = models.TextField()
    image = models.ImageField(upload_to="reciplan/images/")
    url = models.URLField(blank=True)

class Ingredients(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    amt = models.IntegerField()
    unit_of_measure = models.CharField(max_length=10)
    in_cart = models.BooleanField(default=False)

