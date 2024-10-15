from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.user.forms import SignupForm, UpdateForm


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


class UpdateFormTest(TestCase):
    fixtures = ['fixtures/user_fixture.json']
    User = get_user_model()
    data = {
        'email': 'test@example.com',
        'first_name': 'Test',
        'last_name': 'User',
        'cpf': '12345679801',
        'phone': '12345608901',
        'date_birth': '2000-01-01',
        'password': 'newpassword'
    }

    def test_valid_form(self):
        form = UpdateForm(data=self.data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = self.data.copy()
        del data['email']
        form = UpdateForm(data=data)
        self.assertFalse(form.is_valid())

    def test_form_error(self):
        data = self.data.copy()
        data['password2'] = ''
        data['terms'] = False
        form = UpdateForm(data=data)
        for field, msg in form.errors.items():
            self.assertFormError(form, 'form', field, msg)
