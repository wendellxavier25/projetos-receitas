from .base import AUthorsBaseTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class AuthorRegisterTest(AUthorsBaseTest):
    def get_by_placeholder(self, web_element, placeholder):
        return web_element.find_element(By.XPATH, f'//input[@placeholder="{placeholder}"]')

    def fill_form_wendell_data(self, form):
        fields = form.find_elements(By.TAG_NAME, 'input')

        for field in fields:
            if field.is_displayed():
                field.send_keys(' ' * 20)

    def get_form(self):
        return self.browser.find_element(By.XPATH, '/html/body/main/div[2]/form')


    def form_field_test_with_callback(self, callback):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.get_form()

        self.fill_form_wendell_data(form)
        form.find_element(By.NAME, 'email').send_keys('wendellteste@email.com')

        callback(form)
        return form

    def test_empty_username_error_message(self):
        def callback(form):
            first_name_field = self.get_by_placeholder(form, 'Ex: wendell')
            first_name_field.send_keys(' ')
            first_name_field.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn('Write your first name', form.text)
        self.form_field_test_with_callback(callback)


    def test_empty_last_name_error_message(self):
        def callback(form):
            last_name_field = self.get_by_placeholder(form, 'Ex: dev')
            last_name_field.send_keys(' ')
            last_name_field.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn('Write your last name', form.text)
        self.form_field_test_with_callback(callback)


    def test_empty_last_name_error_message(self):
        def callback(form):
            username_field = self.get_by_placeholder(form, 'Your username')
            username_field.send_keys(' ')
            username_field.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn('This field must not be empty', form.text)
        self.form_field_test_with_callback(callback)

    def test_invalid_email_error_message(self):
        def callback(form):
            email_field = self.get_by_placeholder(form, 'Ex: email@email.com')
            email_field.send_keys('email@email.com')
            email_field.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn('Informe um endereço de email válido', form.text)
        self.form_field_test_with_callback(callback)

    def test_passwords_do_not_match(self):
        def callback(form):
            password1 = self.get_by_placeholder(form, 'Type your password')
            password2 = self.get_by_placeholder(form, 'Repeat your password')
            password1.send_keys('Test@123456789')
            password2.send_keys('teste123456')
            password2.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn('Password an password2 must be be equal', form.text)
        self.form_field_test_with_callback(callback)

    
    def test_user_valid_data_register_sucessfully(self):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.get_form()

        self.get_by_placeholder(form, 'Ex: wendell').send_keys('First name')
        self.get_by_placeholder(form, 'Ex: dev').send_keys('Last name')
        self.get_by_placeholder(form, 'Tour username').send_keys('wendelldev')
        self.get_by_placeholder(form, 'Ex: email@email.com').send_keys('email@emailtest.com')
        self.get_by_placeholder(form, 'Type your password').send_keys('wendelldev12@gmail.com')
        self.get_by_placeholder(form, 'Reapeat your password').send_keys('wendelldev12@gmail.com')

        form.submit()

        self.assertIn('Your user is created, please log in', self.browser.find_element(By.TAG_NAME, 'body').text)