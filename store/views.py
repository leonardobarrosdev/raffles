import json
from django.shortcuts import render
from product.models import Product, Image
from .models import Order, OrderItem


def store(request):
	products = Product.objects.all()[:10]
	images = dict()
	for product in products:
		images[product.id] = Image.objects.filter(product=product).first()
	context = {
		'products': products,
		'images': images,
		'is_authenticated': request.user.is_authenticated
	}
	return render(request, 'store/index.html', context)

def cart(request):
	if request.user.is_authenticated:
		customer = request.use.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.get_items_quantity()
	else:
		items = []
		order = {'get_total_price': 0, 'get_items_quantity': 0, 'shipping': False}
	context = {'items': items, 'order': order}
	return render(request, 'store/cart.html', context)

def checkout(request):
	if request.user.is_authenticated:
		customer = request.use.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.get_items_quantity()
	else:
		items = []
		order = {'get_total_price': 0, 'get_items_quantity': 0, 'shipping': False}
	context = {'items': items, 'order': order}
	return render(request, 'store/checkout.html', context)

def update_item(request):
	data = json.loads(request.data)
	product_id = data['productId']
	action = data['action']
	customer = request.user.customer
	product = Product.objects.get(id=product_id)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)
	order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
	if action == 'add':
		order_item.quantity = (order_item.quantity + 1)
	elif action == 'remove':
		order_item.quantity = (order_item.quantity - 1)
	order_item.save()
	if order_item.quantity <= 0:
		order_item.delete()
	return JsonResponse('Item was added', safe=False)
