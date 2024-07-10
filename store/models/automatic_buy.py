from django.db import models
from product.models import Product


class AutomaticBuy(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField(default=0)
	more_popular = models.BooleanField(default=False)

	class Meta:
		verbose_name_plural = 'Automatic Buys'
