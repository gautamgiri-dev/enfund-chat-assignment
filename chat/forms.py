from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SimpleUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']

    def clean_password2(self):
        # Skip password matching validation
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        # Basic password check
        if not password1 or not password2:
            raise forms.ValidationError("Both password fields are required.")
        if password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        
        return password2