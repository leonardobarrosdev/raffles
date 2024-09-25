from django.test import TestCase
from django.contrib.auth import get_user_model


class UserModelTest(TestCase):
	fixtures = ['fixtures/user_fixture.json']

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

	def test_create_user_success(self):
		user = self.User.objects.create_user(**self.data)
		self.assertFalse(user.is_staff)
		self.assertFalse(user.is_superuser)
		self.assertFalse(user.is_active)

	def test_create_user_error(self):
		data = self.data.copy()
		del data['email']
		data['is_superuser'] = True
		with self.assertRaises((TypeError, ValueError)):
			self.User.objects.create_user(**data)

	def test_create_superuser_success(self):
		user = self.User.objects.create_superuser(**self.data)
		self.assertTrue(user.is_staff)
		self.assertTrue(user.is_superuser)
		self.assertFalse(user.is_active)

	def test_create_superuser_error(self):
		data = self.data.copy()
		del data['password']
		data['is_superuser'] = False
		with self.assertRaises((TypeError, ValueError)):
			self.User.objects.create_superuser(**data)

	def test_user_obj_field(self):
		user = self.User.objects.get(pk=2)
		field_label = user._meta.get_field('email').verbose_name
		max_length = user._meta.get_field('email').max_length
		self.assertTrue(isinstance(user, self.User))
		self.assertEqual(field_label, 'email')
		self.assertEqual(max_length, 254)
		self.assertEqual(str(user), user.first_name)
