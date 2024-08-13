from django import forms
from django.contrib.auth.models import User



def add_attr(field, attr_name, attr_new_val):
    existing_attr = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attr} {attr_new_val}'.strip()

def add_placeholder(field, placeholder_val):
    field.widget.attrs['placeholder'] = placeholder_val

class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'],'Your username')
        add_placeholder(self.fields['email'], 'Ex: email@email.com')
        add_placeholder(self.fields['first_name'], 'Ex: wendell')
        add_placeholder(self.fields['last_name'], 'Ex: dev')



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