#File:       urls.py
#Authors:    Joshua Coe, Scott McClure, Danita Hodges
#Purpose:    Define url paths for ReciPlan app
##Version:   1.1
#Version Notes:
#            1.0 - JC - Initial creation
#            1.1 - DH - Grocery list path
#            1.2 - DH - Change password path


from django.urls import path, include
from django.contrib.auth.decorators import login_required
from . import views
from django.contrib.auth import views as view

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', login_required(views.RecipeCreate.as_view()), name='create'),
    #add the paths for the builtin Django user functions
    path("accounts/", include("django.contrib.auth.urls")),
    path("register/", views.register, name="register"),
    path("search/", views.search, name="search"),
    path("recipe/(?<id>\*)", views.detail, name="detail"),
    path("reciplan/home", views.home, name='home'),
    path('grocery_list/', views.grocery, name='grocery'),
    path("password_reset/", login_required(view.PasswordResetView.as_view()), name="password_reset")
]