from django.db import models
from django.contrib.auth import get_user_model
from apps.product.models import Product


class Raffle(models.Model):
	customer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	number = models.PositiveIntegerField()

	def __str__(self):
		return f"Raffle {self.number} for {self.product.title}"
