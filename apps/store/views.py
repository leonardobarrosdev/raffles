import json, mercadopago, qrcode

import ipdb
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_http_methods

from core import settings
from apps.product.models import Product, Image
from apps.raffle.models import Raffle
from .models import Order, ShippingAddress, OrderRaffle
from .forms import ShippingAddressForm
from .utils import get_cart_data


def store(request):
	images = dict()
	products = Product.objects.all()
	for product in products:
		images[product.id] = Image.objects.filter(product=product).first()
	context = {'products': products, 'images': images}
	return render(request, 'store/index.html', context)

def cart(request):
	context = get_cart_data(request)
	return render(request, 'store/cart.html', context)

@login_required
@require_http_methods('POST')
def add_subitems(request, product_id):
	customer = request.user
	try:
		numbers = json.loads(request.COOKIES['numbers'])
		product = Product.objects.get(id=product_id)
		order, created = Order.objects.get_or_create(customer=customer, status='P')
		for number in numbers:
			raffle = Raffle.objects.create(product=product, number=number)
			OrderRaffle.objects.create(order=order, raffle=raffle)
		data = {'order_id': order.id, 'item_title': product.title, 'subitems': numbers}
		return JsonResponse(data, safe=True)
	except KeyError:
		return JsonResponse({'error': 'Numbers cookie missing'}, status=400)
	except Product.DoesNotExist:
		return JsonResponse({'error': 'Product not found'}, status=404)

def process_payment(request):
	sdk = mercadopago.SDK("ENV_ACCESS_TOKEN")
	order = Order.objects.get(customer=request.user)
	# items = data.items
	shipping = ShippingAddress.objects.get(order=order)
	request_options = mercadopago.config.RequestOptions()
	request_options.custom_headers = {
	    'x-idempotency-key': '<SOME_UNIQUE_VALUE>'
	}
	payment_data = {
	    "transaction_amount": order.get_total_price,
	    "description": "Título do produto",
	    "payment_method_id": "pix",
	    "payer": {
	        "email": request.user.email,
	        "first_name": request.user.first_name,
	        "last_name": request.user.last_name,
	        "identification": {
	            "type": "CPF",
	            "number": request.user.cpf
	        },
	        "address": {
	            "zip_code": shipping.zipcode,
	            "street_name": shipping.address,
	            "street_number": shipping.number,
	            "neighborhood": shipping.neighborhood,
	            "city": shipping.city,
	            "federal_unit": shipping.state
	        }
	    }
	}
	payment_response = sdk.payment().create(payment_data, request_options)
	payment = payment_response["response"]
	return json.loads(payment)

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


class CheckoutView(LoginRequiredMixin, View):
	login_url = settings.LOGIN_URL
	redirect_field_name = "user:signin"
	template_name = 'store/checkout.html'

	def get(self, request):
		context = {}
		try:
			context['order'] = Order.objects.get(customer=request.user)
			context['items'] = Order.orderraffle_set.all()
			shipping, created = ShippingAddress.objects.get_or_create(customer=request.user)
			context['form_shipping'] = ShippingAddressForm(instance=shipping)
		except Order.DoesNotExist:
			context = cookie_cart_raffle(request)
			context['form_shipping'] = ShippingAddressForm()
		return render(request, self.template_name, context)

	def post(self, request):
		payment = process_payment(request)
		transation_data = payment.point_of_interaction.transaction_data
		img = qrcode.make(transation_data.qr_code_base64)
		img.save(f'order_{request.user.id}.png')
		context = {'image': img, 'qr_code': transation_data.qr_code}
		return render(request, 'partials/mercadopago.html', context)
	
	def patch(self, request):
		form = ShippingAddressForm(request.POST or None)
		if form.is_valid():
			form.save()
			return render(request, 'partials/mercadopago.html')
		return render(request, 'partials/address.html', {'form_shipping': form})
		
