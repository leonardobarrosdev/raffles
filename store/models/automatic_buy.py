from django.db import models
from raffle.models import Raffle


class AutomaticBuy(models.Model):
	product = models.ForeignKey(Raffle, on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField(default=0)
	more_popular = models.BooleanField(default=False)

	class Meta:
		verbose_name_plural = 'Automatic Buys'
