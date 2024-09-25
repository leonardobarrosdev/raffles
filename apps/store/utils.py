import json, urllib
from apps.product.models import Product
from .models import Order, OrderItem, OrderRaffle


def cookie_cart_raffle(request):
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

def cart_data_raffle(request):
	if request.user.is_authenticated:
		customer = request.user
		try:
			order, created = Order.objects.get_or_create(customer=customer, status='P')
			items = order.orderraffle_set.all()
			return {'order': order, 'items': items}
		except Order.DoesNotExist:
			return cookie_cart_raffle(request)
	return cookie_cart_raffle(request)

def cookie_set_subitems(request, product_id):
	order = {'get_total_price': 0, 'get_items_quantity': 0, 'shipping': False}
	items = []
	subitems = {}
	try:
		decoded_json = urllib.parse.unquote(request.COOKIES.get("cart"))
		cart = json.loads(decoded_json)
		for item_id, numbers in cart.items():
			product = Product.objects.get(id=item_id)
			subitems[item_id] = [Raffle.objects.create(product=product, number=number) for number in numbers]
			items.append(product)
			order['get_total_price'] += product.price * len(numbers)
			order['get_items_quantity'] += len(numbers)
	except:
		return {'order': order, 'items': items, 'subitems': subitems}
	return {'order': order, 'items': items, 'subitems': subitems}

def set_subitems(request, product_id):
	if request.user.is_authenticated:
		customer = request.user
		items = []
		subitems = {}
		try:
			numbers = request.body['numbers']
			product = Product.objects.get(id=product_id)
			order, created = Order.objects.get_or_create(customer=customer, status='P')
			subitems[product_id] = [Raffle.objects.create(product=product, number=number) for number in numbers]
			for subitem in subitems.values():
				order_raffle = OrderRaffle.objects.create(
					order=order,
					product=product,
					raffle=subitem,
					quantity=1
				)
				items.append(order_raffle)
			return {'order': order, 'items': items, 'subitems': subitems}
		except error:
			return {}
	return cookie_add_subitems(request, product_id)

def quest_order(request, data):
	name = data['form']['name']
	email = data['form']['email']
	cookie_data = cookie_cart(request)
	items = cookie_data['items']
	customer, created = User.objects.get_or_create(
		email=email,
	)
	customer.save()
	order = Order.objects.create(
		customer=customer,
		complete=False
	)
	for item in items:
		product = Product.objects.get(id=item.id)
		order_item = OrderItem.objects.create(
			product=product,
			order=order,
			quantity=(item.quantity if item.quantity > 0 else -1 * item.quantity)
		)
	return customer, order
