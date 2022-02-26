#File:       admin.py
#Authors:    Joshua Coe, Scott McClure, Danita Hodges
#Purpose:    Define models for ReciPlan app
##Version:   1.2
#Version Notes:
#            1.0 - JC - Initial creation, registration
#            1.1 - SM - Ingredients registration
#            1.2 - DH - Directions registration

from django.contrib import admin
from .models import Recipe, Ingredients, Direction

admin.site.register(Recipe)
admin.site.register(Ingredients)
admin.site.register(Direction)