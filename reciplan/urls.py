from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create_recipe, name='create'),
    #add the paths for the builtin Django user functions
    path("accounts/", include("django.contrib.auth.urls")),
    path("register/", views.register, name="register"),
    path("search/", views.search, name="search"),
    path("recipe/(?<name>\*)", views.detail, name="detail"),
]