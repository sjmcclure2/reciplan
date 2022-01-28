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
        print('in valid')
        context = self.get_context_data()
        ingredients = context['Ingredients']
        with transaction.atomic():
            self.object = form.save()
            if ingredients.is_valid():
                ingredients.instance = self.object
                ingredients.save()
        return super(RecipeCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('detail', kwargs={'name':self.object.title})
    



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
    ingredients = Ingredients.objects.filter(recipe = results)
    if request.method == 'GET':
        return render(request, 'reciplan/recipe_view.html', {'recipe':results, \
                                                                'ingredients':ingredients, \
                                                                    'yield': results.o_yield, \
                                                                        'targs':ingredients})
    else:
        targs = Ingredients.objects.filter(recipe = results).values('name', 'amt', 'unit_of_measure')
        for i in targs:
            if i['name']=='Flour':
                i['amt'] += 1


        return render(request, 'reciplan/recipe_view.html', {'recipe':results, \
                                                                'ingredients':ingredients, \
                                                                    'yield': results.o_yield, \
                                                                        'targs':targs})