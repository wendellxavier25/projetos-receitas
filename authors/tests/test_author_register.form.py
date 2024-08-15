from django.test import TestCase
from authors.forms import RegisterForm
from parameterized import parameterized

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
