from django.test import TestCase
from .models import UserProfile


class UserTestCase(TestCase):
    def setUp(self):
        fixtures = ['user/fixtures/db_admin_fixture.json']

    def test_create(self):
        user = UserProfile.objects.create(
            email="user4@example.com",
            password="123456"
        )
        self.assertEquals(user.email, "user4@example.com")
