from django.db import models
from apps.product.models import Product


class Promotion(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
	amount = models.PositiveIntegerField(default=0)
	price = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
