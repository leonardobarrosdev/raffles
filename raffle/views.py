from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import (
    login_required,
	permission_required
)
from django.contrib import messages
from django.views import View
from django.utils.decorators import method_decorator
from core import settings
from store.models import AutomaticBuy, AwardedQuota, Promotion
from .models import Raffle, Image, Category
from .forms import (
	RaffleForm,
	ImageFormSet,
	AutomaticBuyFormSet,
	PromotionFormSet,
	AwardedQuotaFormSet
)


decorators = [login_required, permission_required]

@login_required(redirect_field_name='signin')
def dashboard(request):
	user = request.user
	if not user.is_authenticated:
		messages.warning(request, "Are you need to logged to exec the requisited page.")
		return redirect(f"{settings.LOGIN_URL}?next={request.path}")
	context = {'raffles': False}
	if user.is_staff:
		context['raffles'] = Raffle.objects.filter(owner=user)
		return render(request, 'admin/dashboard.html', context)
	return render(request, 'admin/dashboard.html', context)

@login_required(redirect_field_name='signin')
def create(request):
	form = RaffleForm(instance=Image)
	if request.method == 'POST':
		form = RaffleForm(request.POST, request.FILES.getlist('image'))
		if form.is_valid():
			raffle = form.save(commit=False)
			raffle.save()
			messages.success(request, "Your Raffle has been created succesfully!")
			return redirect('raffle_list')
		messages.warning(request, "Coudn't save, retry, please!")
	context = {'form': form,}
	return render(request, 'raffle/create.html', context)


@method_decorator(decorators, name='dispatch')
class CreateView(View):
	template_name = 'raffle/create.html'
	categories = Category.objects.all()
	context = {
		'categories': categories
	}

	def get(self, request):
		return render(request, self.template_name, self.context)

	def post(self, request):
		product = self.__save_raffle(request)
		self.__save_images(request, product)
		self.__save_autobuy(request, product)
		self.__save_promotion(request, product)
		self.__save_awardedquota(request, product)
		messages.success(request, "Your Raffle has been created succesfully!")
		return redirect('raffle_list')
	
	def __save_raffle(self, request):
		title = request.POST['title']
		scheduled_date = request.POST['scheduled_date']
		number_quantity = request.POST['number_quantity']
		price = request.POST['price']
		min_quantity = request.POST['min_quantity']
		digital = request.POST['digital']
		description = request.POST['description']
		owner = request.user
		categories = request.POST.getlist('categories')
		raffle = Raffle.objects.create(
			title=title,
			scheduled_date=scheduled_date,
			number_quantity=number_quantity,
			price=price,
			min_quantity=min_quantity,
			digital=digital,
			description=description,
			owner=owner,
		)
		raffle.save()
		for category in categories:
			raffle.add(category=category)

	@classmethod
	def __save_images(cls, request, product):
		images = request.FILES.getlist('image')
		for img in images:
			image = Image(product=product, image=img)
			image.save()
	
	def __save_autobuy(self, request, product):
		quantities = request.POST.getlist("quantity")
		more_populars = request.POST.getlist("more_popular")
		for quantity, more_popular in zip(quantities, more_populars):
			autobuy = AutomaticBuy.objects.create(
				product=product,
				quentity=quantity,
				more_popular=more_popular
			)
			autobuy.save()
	
	def __save_promotion(self, request, product):
		amounts = request.POST.getlist('amount')
		prices = request.POST.getlist('price')
		for amount, price in zip(amounts, prices):
			promotion = Promotion.objects.create(
				product=product,
				amount=amount,
				price=price
			)
			promotion.save()
	
	def __save_awardedquota(self, request, product):
		awardedquota = request.POST['AwardedQuota']
		quota = AwardedQuota.objects.create(
			product=product,
			number=awardedquota
		)
		quota.save()


@login_required(redirect_field_name='signin')
def delete(request, id):
	raffle = get_object_or_404(Raffle, id=id)
	if request.method == 'POST' and request.user.has_perm('delete_raffle'):
		try:
			raffle.delete()
			messages.success(request, "Raffle succesfully deleted!")
			return redirect('raffle_list')
		except Exception as e:
			print("Delete is ", e)
	return render(request, 'raffle/list.html')

@login_required(redirect_field_name='signin')
def update(request, id):
	raffle = get_object_or_404(Raffle, id=id)
	form = RaffleForm(request.POST or None, instance=raffle)
	if request.method == 'POST' and request.user.has_perm('change_raffle') and form.is_valid():
		try:
			form.save()
			messages.success(request, "Raffle succesfully uodated!")
			return redirect('raffle_list')
		except Exception as e:
			print("Update is ", e)
	return render(request, 'raffle/update.html', {'form': form})


@method_decorator(decorators, name='dispatch')
class UpdateView(View):
	template_name = 'raffle/update.html'
	context = {}

	def get(self, request, id):
		raffle = Raffle.objects.get(id=id)
		form = RaffleForm(instance=raffle)
		formset_image = ImageFormSet(request.FILES, instance=raffle)
		formset_autobuy = AutomaticBuyFormSet(instance=raffle)
		formset_promotion = PromotionFormSet(instance=raffle)
		formset_quota = AwardedQuotaFormSet(instance=raffle)
		self.context = {
			'form': form,
			'formset_image': formset_image,
			'formset_autobuy': formset_autobuy,
			'formset_promotion': formset_promotion,
			'formset_quota': formset_quota,
		}
		return render(request, self.template_name, self.context)

	def post(self, request, id):
		raffle = Raffle.objects.get(id=id)
		form = RaffleForm(instance=raffle)
		formset_image = ImageFormSet(request.FILES, instance=raffle)
		formset_autobuy = AutomaticBuyFormSet(instance=raffle)
		formset_promotion = PromotionFormSet(instance=raffle)
		formset_quota = AwardedQuotaFormSet(instance=raffle)
		if not form.is_valid():
			messages.error(request, 'Changes not valids. Retry, please.')
			return render(request, self.template_name, self.context)
		form.save()
		if formset_image.is_valid(): formset_image.save()
		if formset_autobuy.is_valid(): formset_autobuy.save()
		if formset_promotion.is_valid(): formset_promotion.save()
		if formset_quota.is_valid(): formset_quota.save()
		messages.success(request, 'Successfully updated!')
		return redirect(request, 'list')


@login_required(redirect_field_name='signin')
def list(request):
	try:
		user = request.user
		raffles = Raffle.objects.filter(owner=user)
		return render(request, 'raffle/list.html', {'raffles': raffles})
	except:
		return render(request, 'raffle/list.html', {'raffles': ()})

@login_required(redirect_field_name='signin')
def details(request, id):
	user = request.user
	raffle = Raffle.objects.filter(owner=user, id=id)
	return render(request, 'raffle/details.html', {'raffle': raffle})
