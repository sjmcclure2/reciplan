from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('authorized/', views.authorized, name='authorized'),
    path("accounts/", include("django.contrib.auth.urls")),
]