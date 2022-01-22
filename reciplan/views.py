from distutils import errors
from django.shortcuts import render, redirect
from .models import Recipe
from django.contrib.auth import login
from django.urls import reverse
from reciplan.forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'reciplan/home.html')

@login_required
def create_recipe(request):
    #sample of a view that requires login based on the decorator
    #sample database call for all recipes passed
    #in the render request to the template
    if request.method == 'GET':
        return render(request, 'reciplan/create_recipe.html')

#Registration function
def register(request):
    #render form if request is GET
    if request.method == "GET":
        try:
            #Try to get the errors cookie and pass if exists
            form_errors = request.session['errors']
            return render(
                request, "reciplan/register.html",
                {"form": CustomUserCreationForm, "form_errors":form_errors}
            )
        except:
            #if no errors exist pass a clean signup form
            return render(
                request, "reciplan/register.html",
                {"form": CustomUserCreationForm}
            )
    #if request is POST attempt to create new user
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        #print(form.errors)
        form_errors = ""
        for i in form.errors:
            form_errors+=form.errors[i]
        #if user passes validation return to authorized page
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("authorized"))
        else:
        #if user form fails redirect to new register with errors displayed
            request.session['errors'] = form_errors
            return redirect(reverse('register'))
    
def search(request):
    #get the first 5 recipes from the DB
    recipes = Recipe.objects.all()[0:5]
    #if the method is POST take the form input
    if request.method == "POST":
        query_name = request.POST.get('name', None)
        if query_name:
            #query the DB for recipes with a title containing the search term
            results = Recipe.objects.filter(title__contains=query_name)
            #return the search template with the required variables for the display
            return render(request, 'reciplan/search.html', {"results":results, "query":query_name, 'recipes':recipes})
    #if there are no results display all available recipes in a list.
    #these might look good as bootstrap cards, currently limited to 5 recipes but can increase
    return render(request, 'reciplan/search.html', {'recipes':recipes})

def detail(request, name):
    results = Recipe.objects.get(title=name)
    return render(request, 'reciplan/recipe_view.html', {'recipe':results})