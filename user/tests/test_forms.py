from django.test import TestCase
from django.contrib.auth import get_user_model
from user.forms import SignupForm


class SignupFormTest(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.data = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'cpf': '12345679801',
            'phone': '12345608901',
            'date_birth':'2000-01-01',
            'password': 'newpassword'
        }
    
    def test_valid_form(self):
        data = self.data.copy()
        data['password2'] = 'newpassword'
        data['terms'] = True
        form = SignupForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = self.data.copy()
        data['password2'] = 'newpassword'
        data['terms'] = False
        form = SignupForm(data=data)
        self.assertFalse(form.is_valid())

    def test_form_with_invalid_email(self):
        self.User.objects.create_user(**self.data)
        data = self.data.copy()
        data['password2'] = 'newpassword'
        data['terms'] = True
        form = SignupForm(data=data)
        self.assertRaisesMessage(form.is_valid(), 'Email already registered.')
        