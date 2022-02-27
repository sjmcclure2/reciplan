#File:       forms.py
#Authors:    Joshua Coe, Scott McClure, Danita Hodges
#Purpose:    Define forms for ReciPlan app
##Version:   1.3
#Version Notes:
#            1.0 - JC - Initial creation, user creation
#            1.1 - JC - Ingredients form, create recipe form
#            1.2 - DH - Directions form, create recipe field order
#            1.3 - DH - Line spacing changes to recipe creation form

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from reciplan.models import Ingredients, Recipe, Direction
from django.forms.models import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from .custom_layout_object import *
from django import forms

class CustomUserCreationForm(UserCreationForm):
    #check for email used more than once
    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError("the given email is already registered")
        return self.cleaned_data['email']

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)

class RecipeForm(ModelForm):

    def clean_title(self):
        if Recipe.objects.filter(title=self.cleaned_data['title']).exists():
            raise forms.ValidationError("That recipe title already exists, choose another")
        return self.cleaned_data['title']

    class Meta:
        model = Recipe
        fields = ['title','description','o_yield','image','url']

    def __init__(self, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3 create-label'
        self.helper.field_class = 'col-md-9'
        self.helper.layout = Layout(
            Div(
                Field('title'),
                HTML("<br>"),
                Field('description'),
                HTML("<br>"),
                Field('o_yield'),
                HTML("<br>"),
                Field('image'),
                HTML("<br>"),
                Field('url'),
                HTML("<br>"),
                Fieldset('Add Ingredients',
                    Formset('Ingredients')),
                HTML("<br>"),
                Fieldset('Add Directions',
                    Formset('Directions')),
                HTML("<br>"),
                ButtonHolder(Submit('submit', 'save')),
                )
            )

class IngredientsForm(ModelForm):
    class Meta:
        model = Ingredients
        exclude = ()    

class DirectionsForm(ModelForm):
    class Meta:
        model = Direction
        exclude = ()

IngredientsFormSet = inlineformset_factory(
    Recipe, Ingredients, form=IngredientsForm,
    fields=['amt', 'unit_of_measure', 'name'], extra=1, can_delete=True
)

DirectionsFormSet = inlineformset_factory(
    Recipe, Direction, form = DirectionsForm,
    fields = ['instruction'], extra = 1, can_delete=True
)