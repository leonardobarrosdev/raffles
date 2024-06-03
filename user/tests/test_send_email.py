from django.test import TestCase
from user.views import send_email_welcome


class SendEmailUseCase(TestCase):
	def setUp(self):
		self.moked_fname = 'Remone'
		self.moked_email = 'remone6425@qiradio.com'

	def test_send_mail(self):
		response = send_email_welcome(
			first_name=self.moked_fname,
			email=self.moked_email)
		self.assertTrue(response)
