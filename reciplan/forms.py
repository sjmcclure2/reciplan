from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from reciplan.models import Ingredients, Recipe
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
    class Meta:
        model = Recipe
        fields = ['title','o_yield','image','url','directions','description']

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
                Field('o_yield'),
                Field('image'),
                Field('url'),
                Fieldset('Add Ingredients',
                    Formset('Ingredients')),
                Field('directions'),
                Field('description'),
                HTML("<br>"),
                ButtonHolder(Submit('submit', 'save')),
                )
            )

class IngredientsForm(ModelForm):
    class Meta:
        model = Ingredients
        exclude = ()

        

IngredientsFormSet = inlineformset_factory(
    Recipe, Ingredients, form=IngredientsForm,
    fields=['name','amt','unit_of_measure'], extra=1, can_delete=True
)