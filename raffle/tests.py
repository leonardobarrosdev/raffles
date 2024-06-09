from django.test import TestCase, Client
from datetime import datetime, date
import random
from user.models import UserProfile

NUMBER_QUANTITY = {
	1: 100,
	2: 200,
	3: 500,
	4: 1000,
	5: 10000,
	6: 1000000
}

class RaffleTest(TestCase):
	def setUp(self):
		self.client = Client()

	def test_list(self):
		response = self.client.get("/raffle/list/")
		self.assertEquals(response.status_code, 302)

	def test_create(self):
		response = self.client.post(
			"/raffle/create/",
			{
				"title": "Kit beautfull",
				"scheduled_date": date_generator(2025),
				"number_quantity": random.choice(list(NUMBER_QUANTITY.keys())),
				"category": "Health",
				"price": 0.40,
				"min_quantity": 8,
				"digital": False,
				"description": "Kit beautfull for woman",
				"owner": UserProfile.objects.first(),
			},
			headers={"accept": "application/json"},
		)
		self.assertEquals(response.status_code, 200)


def date_generator(year=datetime.now().year):
	day = random.randint(1, 28)
	month = random.randint(1, 12)
	hours = random.randint(1, 24)
	minutes = random.randint(0, 59)
	seconds = random.randint(0, 59)
	data = "{}-{}-{} {}:{}:{}".format(day, month, year, hours, minutes, seconds)
	return datetime.strptime(data, "%d-%m-%Y %H:%M:%S")