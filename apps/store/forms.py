from django import forms
from .models import ShippingAddress


style_input = 'form-control mb-3'

class ShippingAddressForm(forms.ModelForm):
	class Meta:
		model = ShippingAddress
		fields = ['address', 'number', 'city', 'state', 'zipcode']
		labels = {
			'address': 'Endereço',
			'number': 'Número',
			'city': 'Cidade',
			'state': 'Estado',
			'zipcode': 'CEP'
		}
		widgets = {
			'address': forms.TextInput(attrs={'class': style_input}),
			'number': forms.NumberInput(attrs={'class': style_input}),
			'city': forms.TextInput(attrs={'class': style_input}),
			'state': forms.TextInput(attrs={'class': style_input}),
			'zipcode': forms.TextInput(attrs={'class': style_input})
		}