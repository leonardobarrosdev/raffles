from django.test import TestCase
from django.contrib.auth import get_user_model


class UserModelTest(TestCase):
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

	def test_create_user(self):
		user = self.User.objects.create_user(**self.data)
		self.assertTrue(isinstance(user, self.User))
		self.assertFalse(user.is_staff)
		self.assertFalse(user.is_superuser)
		self.assertEqual(user.__str__(), 'Test')
	
	def test_new_user_is_inactive(self):
		user = self.User.objects.create_user(**self.data)
		self.assertFalse(user.is_active)

	def test_create_superuser(self):
		superuser = self.User.objects.create_superuser(**self.data)
		self.assertTrue(superuser.is_staff)
		self.assertTrue(superuser.is_superuser)
