from django.db import models
from django.contrib.auth import get_user_model
from raffle.models import Raffle


class Order(models.Model):
	PAYMENT_STATUS = [
		('P', 'Pending'),
		('C', 'Complete'),
		('F', 'Failed'),
	]
	customer = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
	status = models.CharField(max_length=50, choices=PAYMENT_STATUS, default='P')
	date_orderd = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.status

	@property
	def shipping(self):
		shipping = False
		order_items = self.orderitems_set.all()
		for order_item in order_items:
			if order_item.raffle.digital == False:
				shipping = True
		return shipping

	@property
	def get_total_price(self):
		order_items = self.OrderItem.all()
		total = sum([item.get_total() for item in order_items])
		return total

	@property
	def get_items_quantity(self):
		order_items = self.OrderItem.all()
		total = sum([item.quantity for item in order_items])
		return total


class OrderItem(models.Model):
	product = models.ForeignKey(Raffle, on_delete=models.PROTECT)
	order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name="items")
	quantity = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.product.name

	@property
	def get_total(self):
		total = self.quantity * self.product.price
		return total
