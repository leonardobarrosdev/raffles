from django.test import TestCase
from django.contrib.auth import get_user_model


class UserModelTest(TestCase):
	def setUp(self):
		self.User = get_user_model()
		self.user = self.User.objects.create_user(
			email="test@example.com",
			password="testpassword",
			first_name="John",
			last_name="Doe",
			cpf="12345678901",
			phone="1234567890",
			date_birth="1990-01-01",
			is_staff=True,
		)

	def test_create_user(self):
		self.assertEqual(self.user.email, "test@example.com")
		self.assertTrue(self.user.check_password("testpassword"))
		self.assertEqual(self.user.first_name, "John")
		self.assertEqual(self.user.last_name, "Doe")
		self.assertEqual(self.user.cpf, "12345678901")
		self.assertEqual(self.user.phone, "1234567890")
		self.assertEqual(str(self.user.date_birth), "1990-01-01")
		self.assertTrue(self.user.is_staff)
		self.assertFalse(self.user.is_superuser)

	def test_create_superuser(self):
		superuser = self.User.objects.create_superuser(
			email="admin@example.com",
			password="adminpassword",
			first_name="Admin",
			last_name="User",
			cpf="98765432109",
			phone="0987654321",
			date_birth="1980-01-01",
		)
		self.assertEqual(superuser.email, "admin@example.com")
		self.assertTrue(superuser.check_password("adminpassword"))
		self.assertEqual(superuser.first_name, "Admin")
		self.assertEqual(superuser.last_name, "User")
		self.assertEqual(superuser.cpf, "98765432109")
		self.assertEqual(superuser.phone, "0987654321")
		self.assertEqual(str(superuser.date_birth), "1980-01-01")
		self.assertTrue(superuser.is_staff)
		self.assertTrue(superuser.is_superuser)

	def test_str_representation(self):
		self.assertEqual(str(self.user), "John")