import uuid
from django.db import models
from django.contrib.auth import get_user_model
from raffle.models import Raffle


class Cart(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True, related_name="items")
    product = models.ForeignKey(Raffle, on_delete=models.CASCADE, blank=True, null=True, related_name="cartitems")
    quantity = models.PositiveSmallIntegerField(default=0)


class Order(models.Model):
    PAYMENT_STATUS = [
        ('P', 'Pending'),
        ('C', 'Complete'),
        ('F', 'Failed'),
    ]
    owner = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    status = models.CharField(max_length=50, choices=PAYMENT_STATUS, default='P')
    placed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.status

    @property
    def total_price(self):
        items = self.items.all()
        total = sum([item.quantity * item.product.price for items in items])
        return total


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name="items")
    product = models.ForeignKey(Raffle, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.product.name
