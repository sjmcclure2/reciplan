
from django.contrib.auth.forms import UserCreationForm, forms
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    #check for email used more than once
    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError("the given email is already registered")
        return self.cleaned_data['email']

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)
