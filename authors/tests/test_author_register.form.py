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
    def test_first_name_placeholder_is_correct(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(current_placeholder, placeholder)
