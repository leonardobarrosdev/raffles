import json
from django.shortcuts import render
from django.views import View
from product.models import Product, Image
from .models import Order, OrderItem


def store(request):
	products = Product.objects.all()[:10]
	images = dict()
	for product in products:
		images[product.id] = Image.objects.filter(product=product).first()
	context = {
		'products': products,
		'images': images
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


class RaffleView(View):
	template_name = 'store/raffle.html'
	context = {}

	def get(self, request, id):
		try:
			product = Product.objects.get(id=id)
			images = Image.objects.filter(product=product)
			self.context['product'] = product
			self.context['images'] = images
			return render(request, self.template_name, self.context)
		except raffle.DoesNotExist:
			message.error(request, 'Raffle does not exist.')
			return redirect(request, 'store:index')