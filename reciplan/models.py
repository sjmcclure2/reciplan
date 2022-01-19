from django.db import models

# Create your models here.
class Recipe(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    ingredients = models.CharField(max_length=500)
    image = models.ImageField(upload_to="reciplan/images/")
    url = models.URLField(blank=True)
