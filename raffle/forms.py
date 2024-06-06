from django import forms
from django.forms import inlineformset_factory
from .models import Category, Raffle, Image
from store.models import AutomaticBuy, AwardedQuota, Promotion


class_default = 'form-control mb-3'


class RaffleForm(forms.ModelForm):
	class Meta:
		model = Raffle
		fields = ['title', 'scheduled_date', 'number_quantity', 'category', 'price', 'min_quantity', 'digital', 'description', 'owner']
		# exclude = ['owner']
		labels = {
			'title': 'Nome da Rifa',
			'scheduled_date': 'Data',
			'number_quantity': 'Quantidade de números',
			'category': 'Catégorias',
			'price': 'Preço',
			'min_quantity': 'Quantidade mínima',
			'digital': 'Typo de produto',
			'description': 'Descrção',
		}
		widgets = {
			'title': forms.TextInput(attrs={'class': class_default}),
			'scheduled_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': class_default}),
			'number_quantity': forms.Select(attrs={'class': class_default}),
			'category': forms.Select(attrs={'class': 'form-control mb-3'}),
			'price': forms.TextInput(attrs={'class': class_default}),
			'min_quantity': forms.NumberInput(attrs={'class': class_default}),
			'digital': forms.NullBooleanSelect(attrs={'class': class_default}),
			'description': forms.Textarea(attrs={'class': class_default, 'rows': 3, 'cols': 50, 'aria-describedby': 'Descrição de Rifa'}),
			'owner': forms.TextInput(attrs={'hidden': True})
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
			attrs={'class': class_default}),
		'more_popular': forms.TextInput(
			attrs={'type': 'radio', 'class': 'form-check-input mb-3'}),
	},
	extra=4,
	can_delete=False
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
	},
	extra=1,
	can_delete=False
)

AwardedQuotaFormSet = inlineformset_factory(
	Raffle,
	AwardedQuota,
	fields = ['number'],
	widgets = {
		'number': forms.NumberInput(
			attrs={'type': 'number', 'class': class_default}),
	},
	extra=1,
	can_delete=False
)