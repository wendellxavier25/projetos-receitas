from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Repeat your password'}),
                                           error_messages={'required': 'Password must not be empty'})

    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Repeat your password'}))


    class Meta:
        model = User

        fields = ['first_name', 'last_name', 'username', 'email', 'password']

        labels = {'first_name': 'First name', 'last_name': 'Last name', 'username': 'Username',
                  'email': 'E-mail', 'password': 'Password'}
        
        help_texts = {'email': 'The e mail must be valid'}

        error_messages = {'username': {'required': 'This field must not be empty'}}

        widgets = {'password': forms.PasswordInput(attrs={'placeholder': 'type you password here'})}