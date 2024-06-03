from django.test import TestCase
from .models import UserProfile


class UserTestCase(TestCase):
	@classmethod
	def setUp(cls):
		fixtures = ["user/fixtures/db_admin_fixture.json"]
		fields = fixtures[1]["fields"]
		self.user = UserProfile.objects.create(
			email=fields["email"],
			password=fields["password"],
			first_name=fields["first_name"],
			last_name=fields["last_name"],
			cpf=fields["cpf"],
			cellfone=fields["cellfone"],
			date_birth=fields[date_birth],
			is_staff=fields["is_staff"] or False
		)

	def test_str(self):
		self.assertEquals(str(self.user), self.user.first_name)
