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
def authorized(request):
    #sample of a view that requires login based on the decorator
    #sample database call for all recipes passed
    #in the render request to the template
    recipes = Recipe.objects.all()
    return render(request, 'reciplan/authorized.html', {'recipes':recipes})

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
        print(form.errors)
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