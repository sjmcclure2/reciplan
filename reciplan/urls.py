from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('authorized/', views.authorized, name='authorized'),
    #add the paths for the builtin Django user functions
    path("accounts/", include("django.contrib.auth.urls")),
    path("register/", views.register, name="register"),
]