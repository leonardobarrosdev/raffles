import json
from django.shortcuts import render, redirect, render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic.base import View
from product.models import Product, Image
from .models import Raffle


class RaffleView(View):
	template_name = 'store/raffle.html'
	context = {}

	def get(self, request, id):
		try:
			product = Product.objects.get(id=id)
			images = Image.objects.filter(product=product)
			self.context['product'] = product
			self.context['images'] = images
			self.context['datas'] = {
				'id': product.id,
				'numberQuantity': product.get_number_quantity_display(),
				'price': product.price
			}
			return render(request, self.template_name, self.context)
		except product.DoesNotExist:
			message.error(request, 'Raffle does not exist.')
			return redirect(request, 'store:index')

	@login_required(redirect_field_name='user:signin')
	def post(request):
		data = json.loads(request.body)
		customer = request.user
		product = Product.objects.get(id=data.productId)
		numbers = data.numbers
		for number in numbers:
			Raffle.objects.create(
				customer=customer,
				product=product,
				number=number
			)
		return HttpResponse.status_code


def list(request):
	products = Product.objects.all()
	images = dict()
	for product in products:
		images[product.id] = Image.objects.filter(product=product).first()
	context = {'products': products, 'images': images}
	return render(request, 'store/raffles.html', context)
