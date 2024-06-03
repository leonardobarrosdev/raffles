from django.db import models
from raffle.models import Raffle


class AwardedQuota(models.Model):
	product = models.ForeignKey(Raffle, on_delete=models.CASCADE, null=True, blank=True)
	number = models.PositiveIntegerField(default=0)
