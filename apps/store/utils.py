import json, urllib, mercadopago, qrcode, uuid
from apps.product.models import Product
from apps.raffle.models import Raffle
from .models import Order, OrderItem, OrderRaffle
from apps.store.models import ShippingAddress


def get_cart_by_cookie(request):
	order = {'get_total_price': 0, 'get_items_quantity': 0, 'shipping': False}
	items = []
	try:
		decoded_json = urllib.parse.unquote(request.COOKIES.get("cart"))
		cart = json.loads(decoded_json).get('cart')
		for item_id, numbers in cart.items():
			product = Product.objects.get(id=int(item_id))
			items.append(product)
			order['get_total_price'] += product.price * len(numbers)
			order['get_items_quantity'] += len(numbers)
		return {'order': order, 'items': items}
	except:
		return {'order': order, 'items': items}

def create_order_by_cookie(request):
	order = {'get_total_price': 0, 'get_items_quantity': 0, 'shipping': False}
	items = []
	try:
		decoded_json = urllib.parse.unquote(request.COOKIES.get('cart'))
		cart = json.loads(decoded_json).get('cart')
		for item_id, numbers in cart.items():
			product = Product.objects.get(id=int(item_id))
			for number in numbers:
				Raffle.objects.create(product=product, number=number)
			items.append(product)
		order = Order.objects.create(custom=request.user, status='P')
		return {'order': order, 'items': items}
	except:
		return {'order': order, 'items': items}

def get_cart_data(request):
	if request.user.is_authenticated:
		customer = request.user
		try:
			order, created = Order.objects.get_or_create(customer=customer, status='P')
			items = order.orderraffle_set.all()
			return {'order': order, 'items': items}
		except Order.DoesNotExist:
			return create_order_by_cookie(request)
	return get_cart_by_cookie(request)

def process_payment(request):
	sdk = mercadopago.SDK("ENV_ACCESS_TOKEN")
	order = Order.objects.get(customer=request.user)
	shipping = ShippingAddress.objects.get(order=order)
	request_options = mercadopago.config.RequestOptions()
	request_options.custom_headers = {
	    'x-idempotency-key': uuid.uuid4()
	}
	payment_data = {
	    "transaction_amount": order.get_total_price,
	    "description": order.product.title,
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
