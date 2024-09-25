from django.db import models
from django.contrib.auth import get_user_model
from apps.store.models.order import Order


class ShippingAddress(models.Model):
	customer = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
	address = models.CharField(max_length=300)
	number = models.PositiveSmallIntegerField()
	neighborhood = models.CharField(max_length=220, null=True, blank=True)
	city = models.CharField(max_length=200)
	state = models.CharField(max_length=2)
	zipcode = models.IntegerField()
	create_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'{self.city} - {self.state}'
