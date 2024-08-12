from django.contrib.auth import get_user_model
from django import forms
from django.utils.translation import gettext_lazy as _


class UserProfileForm(forms.ModelForm):
	password2 = forms.CharField(
		label='Repita a senha',
		max_length=128,
		help_text='Digite a senha',
		widget=forms.PasswordInput(attrs={'type': 'password', 'class': 'form-control'})
	)
	terms = forms.BooleanField(
		label='Você concorda com os termos e serviços dessa plataforma?',
		widget=forms.CheckboxInput(attrs={'type': 'checkbox', 'class': 'form-check-input'})
	)

	class Meta:
		model = get_user_model()
		fields = ['first_name', 'last_name', 'email', 'cpf', 'phone', 'date_birth', 'password', 'password2', 'terms']
		labels = {
			'first_name': 'Nome',
			'last_name': 'Sobrenome',
			'email': 'E-mail',
			'cpf': 'CPF',
			'phone': 'Telefone',
			'date_birth': 'Data de nescimento',
			'password': 'Senha'
		}
		widgets = {
			'first_name': forms.TextInput(attrs={'class': 'form-control'}),
			'last_name': forms.TextInput(attrs={'class': 'form-control'}),
			'email': forms.EmailInput(attrs={'type': 'email', 'class': 'form-control'}),
			'cpf': forms.TextInput(attrs={'type': 'cpf', 'class': 'form-control'}),
			'phone': forms.TextInput(attrs={'type': 'tel', 'class': 'form-control', 'minlength': 9, 'maxlength': 14}),
			'date_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
			'password': forms.PasswordInput(attrs={'type': 'password', 'class': 'form-control'})
		}
		help_texts = {
			'first_name': _('Name'),
			'last_name': _('Last name'),
			'email': 'E-mail',
			'cpf': 'CPF',
			'phone': _('Cell phone'),
			'date_birth': _('Date of birth'),
			'password': _('Password'),
			'password2': _('Password replay'),
		}
		# error_messages = {
		# 	'first_name': _('Name error'),
		# 	'last_name': _('Last name error'),
		# 	'email': _('E-mail error'),
		# 	'cpf': _('CPF error'),
		# 	'phone': _('Cell phone error'),
		# 	'date_birth': _('Date of birth is not valid'),
		# 	'password': _('Password error'),
		# 	'password2': _('password2 error'),
		# 	'terms': _('You need check this field')
		# }
