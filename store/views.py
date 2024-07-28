import json
from django.shortcuts import render
from django.core.serializers import serialize
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from product.models import Product, Image
from raffle.models import Raffle
from .models import Order, OrderItem, OrderRaffle
from .utils import cart_data_raffle


def store(request):
	images = dict()
	products = Product.objects.all()
	for product in products:
		images[product.id] = Image.objects.filter(product=product).first()
	context = {'products': products, 'images': images}
	return render(request, 'store/index.html', context)

def cart(request):
	context = cart_data_raffle(request)
	return render(request, 'store/cart.html', context)

def add_subitems(request, product_id):
	data = set_subitems(request, product_id)
	return JsonResponse(data, safe=False)

def checkout(request):
	context = cart_data(request)
	return render(request, 'store/checkout.html', context)

@login_required(redirect_field_name='user:signin')
def process_mercadopago(request):
	import mercadopago

	sdk = mercadopago.SDK("ACCESS_TOKEN")
	request_options = mercadopago.config.RequestOptions()
	request_options.custom_headers = {
	    'x-idempotency-key': '<SOME_UNIQUE_VALUE>'
	}
	payment_data = {
	   "transaction_amount": float(request.POST.get("transaction_amount")),
	   "token": request.POST.get("token"),
	   "description": request.POST.get("description"),
	   "installments": int(request.POST.get("installments")),
	   "payment_method_id": request.POST.get("payment_method_id"),
	   "payer": {
	       "email": request.POST.get("email"),
	       "identification": {
	           "type": request.POST.get("type"), 
	           "number": request.POST.get("number")
	       }
	   }
	}
	payment_response = sdk.payment().create(payment_data, request_options)
	payment = payment_response["response"]
	print(payment)
	return payment

@login_required(redirect_field_name='user:signin')
def process_order(request):
	data = json.loads(request.body)
	customer = request.user
	order, created = Order.objects.get_or_create(customer=customer)
	total = float(data['form']['total'])
	if total == float(order.get_total_price):
		order.status = 'C'
	order.save()
	if order.shipping == True:
		ShippingAddress.objects.create(
			customer=customer,
			order=order,
			address=data['shipping']['address'],
			number=data['shipping']['number'],
			city=data['shipping']['city'],
			state=data['shipping']['state'],
			zipcode=data['shipping']['zipcode']
		)
	return JsonResponse(f'Payment {order.get_status_display()}.', safe=True)
