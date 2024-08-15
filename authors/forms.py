import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError



def add_attr(field, attr_name, attr_new_val):
    existing_attr = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attr} {attr_new_val}'.strip()

def add_placeholder(field, placeholder_val):
    field.widget.attrs['placeholder'] = placeholder_val


def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError(('Password must have at least one uppercase letter'
                               'one lowercase letter and one number. The length should be'
                               'at least 8 characters'), code='Invalid')

class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'],'Your username')
        add_placeholder(self.fields['email'], 'Ex: email@email.com')
        add_placeholder(self.fields['first_name'], 'Ex: wendell')
        add_placeholder(self.fields['last_name'], 'Ex: dev')
        add_placeholder(self.fields['password'], 'Type you password')
        add_placeholder(self.fields['password2'], 'Repeat you password')



    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': 'your password'}),
                                           error_messages={'required': 'Password must not be empty'}, help_text=('Password must have at least one uppercase letter'
                               'one lowercase letter and one number. The length should be'
                               'at least 8 characters'), validators=[strong_password])

    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Repeat your password'}))


    class Meta:
        model = User

        fields = ['first_name', 'last_name', 'username', 'email', 'password']

        labels = {'first_name': 'First name', 'last_name': 'Last name', 'username': 'Username',
                  'email': 'E-mail', 'password': 'Password'}
        
        help_texts = {'email': 'The e mail must be valid'}

        error_messages = {'username': {'required': 'This field must not be empty'}}

        widgets = {'password': forms.PasswordInput(attrs={'placeholder': 'type you password here'})}
    

    def clean_password(self):
        data = self.cleaned_data.get('password')

        return data
    

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            raise ValidationError({'password': 'Password an password2 must be be equal',
                                   'password2': 'Password an password2 must be be equal'})