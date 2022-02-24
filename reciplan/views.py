#File:       views.py
#Authors:    Joshua Coe, Scott McClure, Danita Hodges
#Purpose:    Define views for ReciPlan app
##Version:   1.2
#Version Notes:
#            1.0 - JC - Initial creation, initial functions
#            1.1 - SM - Detail view
#            1.2 - DH - Modified search view to 8
#            1.4 - JC - Removed targs from GET request for detail view


from distutils import errors
from sre_constants import IN
from django.shortcuts import render, redirect
from .models import Recipe, Ingredients
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
        else:
            data['Ingredients'] = IngredientsFormSet()
        return data

    def form_valid(self, form):
        #print('in valid')
        context = self.get_context_data()
        ingredients = context['Ingredients']
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
        query_name = request.POST.get('name', None)
        if query_name:
            #query the DB for recipes with a title containing the search term
            results = Recipe.objects.filter(title__icontains=query_name)
            #return the search template with the required variables for the display
            return render(request, 'reciplan/search.html', {"results":results, "query":query_name, 'recipes':recipes})
    #if there are no results display all available recipes in a list.
    #these might look good as bootstrap cards, currently limited to 8 recipes but can increase
    return render(request, 'reciplan/search.html', {'recipes':recipes})

def detail(request, id):

    results = Recipe.objects.get(id=id)
    ingredients = Ingredients.objects.filter(recipe = results)

    # Shows the recipe requested by the search method
    if request.method == 'GET':
        return render(request, 'reciplan/recipe_view.html', {'recipe':results, \
                                                                'ingredients':ingredients, \
                                                                    'yield': results.o_yield})    
    else: 
        targs = Ingredients.objects.filter(recipe = results).values('name', 'amt', 'unit_of_measure', 'cup_amt')

        for i in targs:
            # If the user wants to see metric measurements, this will convert the updated yield
            # amount into metric
            if request.method == 'POST':
                print(request.POST)
            if request.POST['unit_conv'] == 'Metric':
                for i in targs:
                    converted = conversions.convert_yield(int(request.POST["convert_y"]), i['unit_of_measure'], i['cup_amt'])
                    i['amt'] = converted[0]
                    i['unit_of_measure'] = converted[1]
                    metric = conversions.Convert.metric_imperial(converted[0], converted[1])
                    i['amt'] = metric[0]
                    i['unit_of_measure'] = metric[1]

                output = zip(ingredients, targs)
                return render(request, 'reciplan/recipe_view.html', {'recipe':results, \
                                                                        'ingredients':output, \
                                                                            'yield': results.o_yield, \
                                                                                'targs':targs})
            else:    
                for i in targs:
                    converted = conversions.convert_yield(int(request.POST["convert_y"]), i['unit_of_measure'], i['cup_amt'])
                    i['amt'] = converted[0]
                    i['unit_of_measure'] = converted[1]
                return render(request, 'reciplan/recipe_view.html', {'recipe':results, \
                                                                                'ingredients':ingredients, \
                                                                                    'yield': results.o_yield, \
                                                                                        'targs':targs})

# This should be linked to the checkbox in recipe_view.html
def cart(request):
    #results = Recipe.objects.get(id=id)
    #ingredient = Ingredients.objects.filter(recipe = results)
    
    response = render(request, 'reciplan/cart.html')  
    if request == "POST":
        response.set_cookie('cart', 'These are the items in the cart')

    return response