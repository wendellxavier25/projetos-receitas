import pytest
from .base import AuthorsBaseTest
from django.contrib.auth.models import User
from selenium.webdriver.common.by import By
from django.urls import reverse



@pytest.mark.functional_test
class AuthorsLoginTest(AuthorsBaseTest):
    def test_user_valid_data_can_login_successfully(self):
        string_password = 'pass'
        user = User.objects.create_user(username='wemdell', password=string_password)

        self.browser.get(self.live_server_url + reverse('authors:login'))

        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        username_field = self.get_by_placeholder(form, 'type your username')
        password_field = self.get_by_placeholder(form, 'type your password')

        username_field.send_keys(user.username)
        password_field.send_keys(string_password)

        form.submit()

        self.assertIn(f'Your are logged in with {user.username}.', self.browser.find_element(By.TAG_NAME, 'body').text)

        
