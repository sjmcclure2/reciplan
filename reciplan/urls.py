from django.urls import path, include
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', login_required(views.RecipeCreate.as_view()), name='create'),
    #add the paths for the builtin Django user functions
    path("accounts/", include("django.contrib.auth.urls")),
    path("register/", views.register, name="register"),
    path("search/", views.search, name="search"),
    path("recipe/(?<id>\*)", views.detail, name="detail"),
    path("reciplan/home", views.home, name='home'),
]