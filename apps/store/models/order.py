from django.db import models
from django.contrib.auth import get_user_model
from apps.product.models import Product
from apps.raffle.models import Raffle


class Order(models.Model):
	PAYMENT_STATUS = [
		('P', 'Pending'),
		('C', 'Completed'),
		('F', 'Failed'),
	]
	customer = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
	status = models.CharField(max_length=50, choices=PAYMENT_STATUS, default='P')
	date_ordered = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.status

	@property
	def shipping(self):
		return any(item.product.digital == False for item in self.items.all())

	@property
	def get_total_price(self):
		return sum(item.get_total_price() for item in self.items.all())

	@property
	def get_items_quantity(self):
		return sum(item.quantity for item in self.items.all())


class OrderItem(models.Model):
	order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name="items")
	product = models.ForeignKey(Product, on_delete=models.PROTECT)
	quantity = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.product.title

	@property
	def get_total_price(self):
		return self.quantity * self.product.price


class OrderRaffle(OrderItem):
	raffle = models.ForeignKey(Raffle, on_delete=models.PROTECT)

	def __str__(self):
		return f"Order Raffle for {self.raffle.product.title} with raffle number {self.raffle.number}"
