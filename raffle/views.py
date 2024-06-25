from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import (
	login_required,
	permission_required
)
from django.contrib import messages
from django.views import View
from django.views.decorators.http import require_http_methods
from django.forms import formset_factory, inlineformset_factory
from django.utils.decorators import method_decorator
from core import settings
from user.models import UserProfile
from store.models import AutomaticBuy, AwardedQuota, Promotion
from .models import Raffle, Image, Category
from .forms import (
	RaffleForm,
	ImageForm,
	AutomaticBuyFormSet,
	PromotionFormSet,
	AwardedQuotaFormSet,
	ImageInlineFormSet
)


permissions = ['raffle.*']
decorators = [login_required, permission_required(permissions, raise_exception=True)]

# @method_decorator(decorators, name='dispatch')
class CreateView(View):
	template_name = 'raffle/create.html'
	context = {}

	def get(self, request):
		form = RaffleForm()
		form_image = ImageForm()
		formset_autobuy = AutomaticBuyFormSet()
		formset_promotion = PromotionFormSet()
		formset_quota = AwardedQuotaFormSet()
		self.context = {
			'form': form,
			'form_image': form_image,
			'formset_autobuy': formset_autobuy,
			'formset_promotion': formset_promotion,
			'formset_quota': formset_quota,
		}
		return render(request, self.template_name, self.context)

	def post(self, request):
		form = RaffleForm(request.POST)
		if not form.is_valid():
			self.context['form'] = form
			return render(request, self.template_name, self.context)
		if not request.user.is_authenticated:
			return redirect('signin')
		raffle = form.save(commit=False)
		raffle.owner = request.user
		raffle.save()
		images = request.FILES.getlist('image')
		for image in images:
			Image.objects.create(product=raffle, image=image)
		formset_autobuy = AutomaticBuyFormSet(instance=raffle)
		formset_promotion = PromotionFormSet(instance=raffle)
		formset_quota = AwardedQuotaFormSet(instance=raffle)
		if formset_autobuy.is_valid(): formset_autobuy.save()
		if formset_promotion.is_valid(): formset_promotion.save()
		if formset_quota.is_valid(): formset_quota.save()
		messages.success(request, "Your Raffle has been created succesfully!")
		return redirect('product:list')


# @method_decorator(decorators, name='dispatch')
class UpdateView(View):
	template_name = 'raffle/update.html'
	context = {}

	def get(self, request, id):
		raffle = Raffle.objects.get(id=id)
		images = Image.objects.filter(product=raffle)
		form = RaffleForm(instance=raffle)
		formset_autobuy = AutomaticBuyFormSet(instance=raffle)
		self.context = {
			'form': form,
			'formset_image': ImageInlineFormSet(instance=raffle),
			'formset_autobuy': formset_autobuy,
		}
		return render(request, self.template_name, self.context)

	def post(self, request, id):
		raffle = Raffle.objects.get(id=id)
		instanced_images = Image.objects.filter(product=raffle)
		form = RaffleForm(request.POST, instance=raffle)
		if not form.is_valid():
			messages.error(request, 'Changes not valids. Retry, please.')
			return render(request, self.template_name, self.context)
		raffle = form.save()
		formset_image = ImageInlineFormSet(request.POST, request.FILES, instance=raffle)
		if formset_image.is_valid():
			formset_image.save()
		# queryset = AutomaticBuy.objects.filter(product=raffle)
		# formset_autobuy = AutomaticBuyFormSet(request.POST, queryset=queryset)
		# if formset_autobuy.is_valid(): formset_autobuy.save()
		messages.success(request, 'Successfully updated!')
		return redirect('raffle:list')

	def get_data(self, objects):
		data = {
			'form-TOTAL_FORMS': str(len(objects)),
			'form-INITIAL-FORMS': '1',
		}
		for i, obj in enumerate(objects):
			data[f'form-{i}-image'] = obj.image
		return data

	def get_image_data(self, images):
		data = {
			'form-TOTAL_FORMS': str(len(images)),
			'form-INITIAL-FORMS': '1',
		}
		for image in (images):
			data[image] = images[image]
		return data


@login_required(redirect_field_name='signin')
def list(request):
	try:
		raffles = Raffle.objects.all()
		return render(request, 'raffle/list.html', {'products': raffles})
	except:
		return render(request, 'raffle/list.html', {'products': ()})

@login_required(redirect_field_name='signin')
def details(request, id):
	user = request.user
	raffle = Raffle.objects.filter(owner=user, id=id)
	return render(request, 'raffle/details.html', {'raffle': raffle})

@login_required(redirect_field_name='signin')
@require_http_methods(['DELETE'])
def delete(request, id):
	raffle = get_object_or_404(Raffle, id=id)
	raffle.delete()
	return render(request, 'partials/tbody.html')


class ImageView(View):
	template_name = "partials/form.html"
	context = {
		'form_image': ImageForm(),
	}

	def get(self, request):
		product = request['product']
		if product:
			self.context['images'] = Image.objects.filter(product=product)
		return render(request, self.template_name, self.context)

	def post(self, request):
		product = request['product']
		form_image = ImageForm(request)
		if product and form_image.is_valid():
			image = form_image(commit=False)
			image.product = product
			image.save()
			self.context['images'] += image
			if len(request.FILES) < 5:
				self.context['form_image'] = ImageForm()
			self.context['form_image'] = None
		return render(request, self.template_name, self.context)

	def patch(self, request):
		return render(request, self.template_name, self.context)

	def delete(self, request, id):
		image = get_object_or_404(Image, id=id)
		image.delete()
		self.context['form_image'] = ImageForm()
		return render(request, self.template_name, self.context)