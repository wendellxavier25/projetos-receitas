from django.test import TestCase as DjangoTestCase
from unittest import TestCase
from authors.forms import RegisterForm
from parameterized import parameterized
from django import setup
from django.urls import reverse

class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('username', 'You username'),
        ('email', 'Ex: email@email.com'),
        ('first_name', 'Ex: wendell'),
        ('last_name', 'Ex: dev'),
        ('password', 'Type your password'),
        ('password2', 'Reapeat your password'),
        ])
    def test_fields_placeholder(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(current_placeholder, placeholder)

    @parameterized.expand([
        ('username', ('Obrigatório. 150 caracteres ou menos. Letras, números e @/./+/-/_ apenas.')),
        ('email', 'The e mail must be valid'),
        ('password', ('Password must have at least one uppercase letter'
                               'one lowercase letter and one number. The length should be'
                               'at least 8 characters')),
        
        ])
    def test_fields_help_text(self, field, needed):
        form = RegisterForm()
        current_placeholder = form[field].field.help_text
        self.assertEqual(current_placeholder, needed)

class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs):
        self._form_data = {'username': 'user', 'first_name': 'first', 'last_name': 'last', 
                           'email': 'email@email.com', 'password': 'Test@12345', 'password2': 'Test@12345'}
        return super().setUp(*args, **kwargs)
    
    @parameterized.expand([
        ('username', 'This filed must not be empty'),
        ('first_name', 'Write your first name'),
        ('last_name', 'Write your last name'),
        ('password', 'Password must not be empty'),
        ('password2', 'Please, repeat your password'),
        ('email', 'E-mail is required')
        ])
    def test_fields_cannot_be_empty(self, field, msg):
        self._form_data[field] = ''
        url = reverse('authors:create')
        response = self.client.post(url, data=self._form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))