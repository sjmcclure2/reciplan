#File:       views.py
#Authors:    Joshua Coe, Scott McClure, Danita Hodges
#Purpose:    Define views for ReciPlan app
#Version:   1.7
#Version Notes:
#            1.0 - JC - Initial creation, initial functions
#            1.1 - SM - Detail view
#            1.2 - DH - Modified search view to 8
#            1.3 - JC - Removed targs from GET request for detail view
#            1.4 - DH - Added directions form   
#            1.4 - JC - Removed targs from GET request for detail view
#            1.5 - JC - Updated the conversion implementation
#            1.6 - JC - Updated search algorithm to allow search by ingredient
#            1.7 - DH - Added directions to if-else renders
#            1.8 - JC - Updated search algorith to search both ingredients and titles

from distutils import errors
from sre_constants import IN
from django.shortcuts import render, redirect
from .models import Recipe, Ingredients, Direction
from django.contrib.auth import login
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .forms import *
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.forms.models import model_to_dict
from . import conversions

def index(request):
    #redirect user to login page as first page of the site
    return redirect(reverse('login'))

def home(request):
    return render(request, "reciplan/home.html")

class RecipeCreate(CreateView):
    model = Recipe
    template_name = 'reciplan/create_recipe.html'
    form_class = RecipeForm
    success_url = None

    def get_context_data(self, **kwargs):
        data = super(RecipeCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['Ingredients'] = IngredientsFormSet(self.request.POST)
            data['Directions'] = DirectionsFormSet(self.request.POST)
        else:
            data['Ingredients'] = IngredientsFormSet()
            data['Directions'] = DirectionsFormSet()
        return data

    def form_valid(self, form):
        #print('in valid')
        context = self.get_context_data()
        ingredients = context['Ingredients']
        directions = context['Directions']
        with transaction.atomic():
            self.object = form.save()
            if ingredients.is_valid():
                ingredients.instance = self.object
                new_ingredient = ingredients.save(commit=False)
                for i in new_ingredient:
                    i.cup_amt = \
                        conversions.Convert.to_cups(self.object.o_yield, \
                            i.unit_of_measure, i.amt)
                    i.save()
            if directions.is_valid():
                directions.instance = self.object
                new_direction = directions.save(commit=False)
                counter = 1
                for i in new_direction:
                    print(i)
                    i.step = counter
                    counter += 1
                    i.save()
        return super(RecipeCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('detail', kwargs={'id':self.object.id})

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
            return redirect(reverse("home"))
        else:
        #if user form fails redirect to new register with errors displayed
            request.session['errors'] = form_errors
            return redirect(reverse('register'))
    
def search(request):
    #get the first 8 recipes from the DB
    recipes = Recipe.objects.all()[0:8]

    #if the method is POST take the form input
    if request.method == "POST":
        query_name = request.POST.get('name')
        if query_name:
            #create the results array
            results = []
            #query the DB for ingredients that match the query name
            ingredients = Ingredients.objects.filter(name__contains=query_name)
            #add all recipes containing ingredients to the results
            for i in ingredients:
                results.append(i.recipe)
            #find recipes with a title containing the query name
            titles = Recipe.objects.filter(title__icontains=query_name)
            #add recipes from the title search to the results
            for L in titles:
                results.append(L)
            #return the search template with the required variables for the display
            return render(request, 'reciplan/search.html', {"results":results, "query":query_name, 'recipes':recipes})
    #if there are no results display all available recipes in a list.
    #these might look good as bootstrap cards, currently limited to 8 recipes but can increase
    return render(request, 'reciplan/search.html', {'recipes':recipes})

def detail(request, id):

    results = Recipe.objects.get(id=id)
    ingredients = Ingredients.objects.filter(recipe = results)
    directions = Direction.objects.filter(recipe = results)

    # Shows the recipe requested by the search method
    if request.method == 'GET':
        return render(request, 'reciplan/recipe_view.html', {'recipe':results, \
            'ingredients':ingredients, 'yield': results.o_yield, 'directions':directions}) 

    else: 
        targs = Ingredients.objects.filter(recipe = results).values('name', 'amt', 'unit_of_measure', 'cup_amt')

        for i in targs:
            # If the user wants to see metric measurements, this will convert the updated yield
            # amount into metric
            unit_conv = "Imperial"
            try:
               unit_conv = request.POST['unit_conv']
            except Exception as e:
                pass

            if unit_conv == 'Metric':
                new_yield = request.POST["convert_y"]
                for i in targs:
                    converted = conversions.convert_yield(int(request.POST["convert_y"]), i['unit_of_measure'], i['cup_amt'])
                    i['amt'] = converted[0]
                    i['unit_of_measure'] = converted[1]
                    metric = conversions.Convert.to_metric(converted[0], converted[1])
                    i['amt'] = metric[0]
                    i['unit_of_measure'] = metric[1]
                #create lists for each needed output
                orig_amt = []
                orig_meas = []
                targ_amt = []
                targ_meas = []
                ingredient_list=[]
                #loop through the lists and get what is needed
                for j in range(len(ingredients)):
                    orig_amt.append(ingredients[j].amt)
                    orig_meas.append(ingredients[j].unit_of_measure)
                    ingredient_list.append(ingredients[j].name)
                    targ_amt.append(targs[j]['amt'])
                    targ_meas.append(targs[j]['unit_of_measure'])
                #zip lists into tuples
                zipped = zip(orig_amt,orig_meas,targ_amt,targ_meas,ingredient_list)

                return render(request, 'reciplan/recipe_view.html', 
                                { 
                                    'recipe':results, 
                                    'ingredients':ingredients, 
                                    'yield': results.o_yield, 
                                    'targs':zipped,
                                    'new_yield':new_yield, 
                                    'directions':directions, 
                                    'metric':1, 
                                    'ingredients':ingredients, 
                                    'yield': results.o_yield, 
                                    'targs':zipped,
                                    'new_yield':new_yield
                                }
                              )
            else:    
                new_yield = request.POST["convert_y"]
                for i in targs:
                    converted = conversions.convert_yield(int(request.POST["convert_y"]), i['unit_of_measure'], i['cup_amt'])
                    i['amt'] = converted[0]
                    i['unit_of_measure'] = converted[1]
                    #loop through the lists and get what is needed
                #create lists for each needed output
                orig_amt = []
                orig_meas = []
                targ_amt = []
                targ_meas = []
                ingredient_list=[]
                #loop through the lists and get what is needed
                for j in range(len(ingredients)):
                    orig_amt.append(ingredients[j].amt)
                    orig_meas.append(ingredients[j].unit_of_measure)
                    ingredient_list.append(ingredients[j].name)
                    targ_amt.append(targs[j]['amt'])
                    targ_meas.append(targs[j]['unit_of_measure'])
                #zip lists into tuples
                zipped = zip(orig_amt,orig_meas,targ_amt,targ_meas,ingredient_list)
                return render(request, 'reciplan/recipe_view.html', {'recipe':results, \
                    'ingredients':ingredients, 'yield': results.o_yield, 'targs':zipped,\
                    'new_yield':new_yield, 'directions':directions})

def grocery(request):
    # if method = post
    # print to PDF

    return render(request, 'reciplan/grocery_list.html')