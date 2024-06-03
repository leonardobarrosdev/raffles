from django import forms
from django.forms import inlineformset_factory
from .models import Category, Raffle, Image
from store.models import AutomaticBuy, AwardedQuota, Promotion


class_default = 'form-control mb-3'


class RaffleForm(forms.ModelForm):
	class Meta:
		model = Raffle
		fields = '__all__'
		exclude = ['owner']
		widgets = {
			'title': forms.TextInput(attrs={'class': class_default}),
			'scheduled_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': class_default}),
			'number_quantity': forms.Select(attrs={'class': class_default}),
			'price': forms.TextInput(attrs={'class': class_default}),
			'min_quantity': forms.NumberInput(attrs={'class': class_default}),
			'digital': forms.NullBooleanSelect(attrs={'class': class_default}),
			'description': forms.Textarea(attrs={'class': class_default}),
			'category': forms.SelectMultiple(attrs={'class': 'form-select mb-3', 'size': '3'}),
		}


class ImageForm(forms.ModelForm):
	class Meta:
		model = Image
		fields = ['image']
		widgets = {
			'image': forms.ClearableFileInput(attrs={'allow_multiple_selected': True, 'type': 'file', 'class': 'img-thumbnail mb-3'}),
		}


class AutomaticBuyForm(forms.ModelForm):
	class Meta:
		model = AutomaticBuy
		fields = ['quantity', 'more_popular']
		widgets = {
			'quantity': forms.NumberInput(
				attrs={'class': class_default, 'id': 'radio1'}),
			'more_popular': forms.TextInput(
				attrs={'type': 'radio', 'class': 'form-check-input mb-3', 'id': 'radio1'}),
		}


class CategoryForm(forms.ModelForm):
	class Meta:
		model = Category
		fields = ['name']
		widgets = {
			'name': forms.TextInput(attrs={'class': class_default}),
		}


class PromotionForm(forms.ModelForm):
	class Meta:
		model = Promotion
		fields = ['amount', 'price']
		widgets = {
			'amount': forms.NumberInput(
				attrs={'type': 'number', 'class': class_default}),
			'price': forms.TextInput(
				attrs={'class': 'form-control'}),
		}


class AwardedQuotaForm(forms.ModelForm):
	class Meta:
		model = AwardedQuota
		fields = ['number']
		widgets = {
			'number': forms.NumberInput(
				attrs={'type': 'number', 'class': class_default}),
		}


ImageFormSet = inlineformset_factory(
	Raffle,
	Image,
	fields=['image'],
	widgets = {
		'image': forms.ClearableFileInput(attrs={'allow_multiple_selected': True, 'type': 'file', 'class': 'img-thumbnail mb-3'}),
	}
)

AutomaticBuyFormSet = inlineformset_factory(
	Raffle,
	AutomaticBuy,
	fields=['quantity', 'more_popular'],
	widgets = {
		'quantity': forms.NumberInput(
			attrs={'class': class_default, 'id': 'radio1'}),
		'more_popular': forms.TextInput(
			attrs={'type': 'radio', 'class': 'form-check-input mb-3', 'id': 'radio1'}),
	}
)

PromotionFormSet = inlineformset_factory(
	Raffle,
	Promotion,
	fields = ['amount', 'price'],
	widgets = {
		'amount': forms.NumberInput(
			attrs={'type': 'number', 'class': class_default}),
		'price': forms.TextInput(
			attrs={'class': 'form-control'}),
	}
)

AwardedQuotaFormSet = inlineformset_factory(
	Raffle,
	AwardedQuota,
	fields = ['number'],
	widgets = {
		'number': forms.NumberInput(
			attrs={'type': 'number', 'class': class_default}),
	}
)