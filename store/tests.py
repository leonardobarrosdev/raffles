from django.test import TestCase, RequestFactory
from django.contrib.auth import AnonymousUser
from user.models import UserProfile
from product.models import Product
from .models import Order, OrderItem, OrderRaffle
from .views import CartView


class OrderRaffleTestCase(TestCase):
	def setUp(self):
		self.factory = RequestFactory()
		self.user = User.objects.create_customer(
			email='test@company.com',
			password='123456'
		)
		self.product = Product.objects.get(id=1)

	def test_customer_has_raffle(self):
		request = self.factory.post(f'/cart/{self.product.id}')
		request.user = AnonymousUser()
		# request.body = 
		response = CartView.as_view()(request, self.product.id)
		self.assertEquals(response.status_code, 200)
