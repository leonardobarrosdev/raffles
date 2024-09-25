from django.contrib import admin
from .models import (
	Order,
	OrderItem,
	ShippingAddress,
	AutomaticBuy,
	Promotion,
	AwardedQuota
)

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(AutomaticBuy)
admin.site.register(Promotion)
admin.site.register(AwardedQuota)
