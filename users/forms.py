from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    id_card = forms.ImageField(required=True, help_text="Upload a clear image of your ID card.")
    
    class Meta:
        model = User  # Use your custom User model
        fields = ['username', 'email', 'first_name', 'last_name', 'role', 'phone_number', 'cnic', 'id_card', 'password1', 'password2']
