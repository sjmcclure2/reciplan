from django.shortcuts import render
from .models import Recipe

def index(request):
    recipes = Recipe.objects.all()
    return render(request, 'reciplan/home.html', {'recipes':recipes})

def authorized(request):
    return render(request, 'reciplan/authorized.html')