from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import (
	login_required,
	permission_required
)
from django.contrib import messages
from django.views import View
from django.utils.decorators import method_decorator
from core import settings
from user.models import UserProfile
from store.models import AutomaticBuy, AwardedQuota, Promotion
from .models import Raffle, Image, Category
from .forms import (
	RaffleForm,
	ImageFormSet,
	AutomaticBuyFormSet,
	PromotionFormSet,
	AwardedQuotaFormSet
)

permissions = ['raffle.*']
decorators = [login_required, permission_required(permissions, raise_exception=True)]

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


@method_decorator(decorators, name='dispatch')
class CreateView(View):
	template_name = 'raffle/create.html'
	context = {}

	def get(self, request):
		form = RaffleForm()
		formset_image = ImageFormSet()
		formset_autobuy = AutomaticBuyFormSet()
		formset_promotion = PromotionFormSet()
		formset_quota = AwardedQuotaFormSet()
		self.context = {
			'form': form,
			'formset_image': formset_image,
			'formset_autobuy': formset_autobuy,
			'formset_promotion': formset_promotion,
			'formset_quota': formset_quota,
		}
		return render(request, self.template_name, self.context)

	def post(self, request):
		form = RaffleForm(request.POST, request.FILES.getlist('image'))
		if not form.is_valid():
			self.context['form'] = form
			return render(request, self.template_name, self.context)
		if not request.user.is_authenticated:
			return redirect('signin')
		raffle = form.save()
		formset_image = ImageFormSet(request.FILES, instance=raffle)
		formset_autobuy = AutomaticBuyFormSet(instance=raffle)
		formset_promotion = PromotionFormSet(instance=raffle)
		formset_quota = AwardedQuotaFormSet(instance=raffle)
		if formset_image.is_valid(): formset_image.save()
		if formset_autobuy.is_valid(): formset_autobuy.save()
		if formset_promotion.is_valid(): formset_promotion.save()
		if formset_quota.is_valid(): formset_quota.save()
		messages.success(request, "Your Raffle has been created succesfully!")
		return redirect('raffle_list')


@login_required(redirect_field_name='signin')
def delete(request, id):
	raffle = get_object_or_404(Raffle, id=id)
	if request.method == 'POST' and request.user.has_perm('raffle.delete_raffle'):
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
		formset_image = ImageFormSet(instance=raffle)
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
		form = RaffleForm(request.FILES, instance=raffle)
		if not form.is_valid():
			messages.error(request, 'Changes not valids. Retry, please.')
			return render(request, self.template_name, self.context)
		form.save()
		formset_image = ImageFormSet(request.FILES, instance=raffle)
		formset_autobuy = AutomaticBuyFormSet(instance=raffle)
		formset_promotion = PromotionFormSet(instance=raffle)
		formset_quota = AwardedQuotaFormSet(instance=raffle)
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
