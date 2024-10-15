from django.db import models
from apps.product.models import Product


class Raffle(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	number = models.PositiveIntegerField()

	def __str__(self):
		return f"Raffle {self.number} for {self.product.title}"
