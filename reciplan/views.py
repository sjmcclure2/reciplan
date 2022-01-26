from distutils import errors
from django.shortcuts import render, redirect
from .models import Recipe
from django.contrib.auth import login
from django.urls import reverse
from reciplan.forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required

def index(request):
    #redirect user to login page as first page of the site
    return redirect(reverse('login'))

def home(request):
    return render(request, "reciplan/home.html")

@login_required
def create_recipe(request):
    #send authenticated user to the create recipe page
    #sedn unauthenticated/guest user to login page
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

# Takes in the amount of cups and converts to an appropriate DRY unit based on amount
def update_d_units(cup_amt): 
        # If the amount is 1/4 cup or more, maintain measurement in cups
    if cup_amt >= (1/4):
        unit = 'cup'
        return cup_amt, unit
        # If the amount is less than 1/4 cup but more than 1/8 cup, convert to tbsp
    elif cup_amt < (1/4) and cup_amt >= (1/8):
        unit = 'tbsp'
        return 16 * cup_amt, unit
        # If the amount is less than 1/8 cup, convert to tsp
    else:
        unit = 'tsp'
        return 48 * cup_amt, unit

    # Takes in the amount of cups and converts to an appropriate LIQUID unit based on amount
def update_l_units(cup_amt):
        # If the amt is less than 1 cup, convert to fl oz
    if cup_amt < 1:
        unit = "fl oz"
        return 8 * cup_amt, unit
        # If the amt is between 1 and 4 cups, maintain measurement in cups
    elif cup_amt >= 1 and cup_amt <= 4:
        unit = 'cup'
        return cup_amt, unit
        # if the amt is more than 3 but no more than 8, convert to pints
    elif cup_amt > 5 and cup_amt < 8:
        unit = 'pint'
        return (1/2) * cup_amt, unit
        # If the amt is more than 3 but no more than 15, convert to quarts
    elif cup_amt >= 8 and cup_amt < 16:
        unit = 'quart'
        return (1/4) * cup_amt, unit
        # if the amt is more than 16 cups, convert to gallons
    else:
        unit = 'gallon'
        return (1/16) * cup_amt, unit
    
def update_yield(o_yield, t_yield, unit, amt):
        # Converts the original yield ingredient amount into the target yield amount
    adj_amt = (amt/o_yield) * t_yield

    if unit == "fl oz":
        cup_amt = (1/8) * adj_amt
        output = update_l_units(cup_amt)
        return output
    elif unit == "pint":
        cup_amt = 2 * adj_amt
        output = update_l_units(cup_amt)
        return output
    elif unit == "quart":
        cup_amt = 4 * adj_amt
        output = update_l_units(cup_amt)
        return output
    elif unit == "gallon":
        cup_amt = 16 * adj_amt
        output = update_l_units(cup_amt)
        return output
    elif unit == "tsp":
        cup_amt = (1/48) * adj_amt
        output = update_d_units(cup_amt)
        return output
    elif unit == "tbsp":
        cup_amt = (1/16) * adj_amt
        output = update_d_units(cup_amt)
        return output
    elif unit == "cup":
        cup_amt = adj_amt
        output = update_d_units(cup_amt)
        return output
    elif unit == "l_cup":
        cup_amt = adj_amt
        output = update_l_units(cup_amt)
        return output
    elif unit == "ea":
        return adj_amt, unit
    else:
        return print("Error!")