from datetime import datetime
import random
import ipdb
from django.test import TestCase, Client, tag
from django.urls import reverse
from apps.product.models import Product


NUMBER_QUANTITY = {
	1: 100,
	2: 200,
	3: 500,
	4: 1000,
	5: 10000,
	6: 1000000
}

def date_generator(year=datetime.now().year):
	day = random.randint(1, 28)
	month = random.randint(1, 12)
	hours = random.randint(0, 23)
	minutes = random.randint(0, 59)
	seconds = random.randint(0, 59)
	data = "{:02d}-{:02d}-{} {:02d}:{:02d}:{:02d}".format(
		day, month, year, hours, minutes, seconds)
	return datetime.strptime(data, "%d-%m-%Y %H:%M:%S")

class ProductTest(TestCase):
	fixtures = [
		'fixtures/category_fixture.json',
		'fixtures/user_fixture.json',
		'fixtures/product_fixture.json'
	]

	def setUp(self):
		self.client = Client()
		self.data = {
			"title": "Kit beautfull",
			"scheduled_date": date_generator(2025),
			"number_quantity": random.choice(list(NUMBER_QUANTITY.keys())),
			"price": 0.40,
			"min_quantity": 8,
			"digital": False,
			"description": "Kit beautfull for woman",
			"owner": 7,
			"category": 2,
		}
		self.client.login(email="admin@company.com", password="123456")

	def test_create_product_success(self):
		response = self.client.post(
			reverse('product:create'),
			self.data,
			headers={"accept": "application/json"},
		)
		self.assertRedirects(response, reverse('product:list'))
		self.assertEquals(response.status_code, 302)
		self.assertEqual(Product.objects.count(), 11)

	def test_create_product_error(self):
		data = self.data.copy()
		del data['title']
		# with self.assertRaises(ValueError):
		response = self.client.post(reverse('product:create'), data, headers={"accept": "application/json"})
		self.assertNotEquals(response.status_code, 302)

	def test_list_product_success(self):
		response = self.client.get(reverse("product:list"))
		self.assertEquals(response.status_code, 200)

	@tag('details')
	def test_details_product_success(self):
		product = Product.objects.get(pk=1)
		response = self.client.get(reverse('product:details', kwargs={'id': 1}))
		self.assertIs(response.status_code, 200)
		self.assertEqual(product, response.context['product'])

	@tag('details')
	def test_details_product_error(self):
		product = Product.objects.get(pk=2)
		response = self.client.get(reverse('product:details', kwargs={'id': 1}))
		self.assertNotEqual(product, response.context['product'])

	@tag('delete')
	def test_delete_product_success(self):
		response = self.client.delete(reverse('product:delete', kwargs={'id': 9}))
		self.assertEqual(Product.objects.count(), 9)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(reverse('product:list') + 'list.html')

	@tag('delete')
	def test_delete_product_error(self):
		response = self.client.delete(reverse('product:delete', kwargs={'id': 9}))
		self.assertNotEqual(Product.objects.count(), 10)
		self.assertNotEqual(response.status_code, 302)
		self.assertTemplateNotUsed('templates/raffles/delete.html')
