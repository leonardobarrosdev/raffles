from django.contrib.auth import get_user_model
from django import forms
from django.utils.translation import gettext_lazy as _

WIDGETS = {
	'first_name': forms.TextInput(attrs={'class': 'form-control'}),
	'last_name': forms.TextInput(attrs={'class': 'form-control'}),
	'email': forms.EmailInput(attrs={'type': 'email', 'class': 'form-control'}),
	'cpf': forms.TextInput(attrs={'type': 'cpf', 'class': 'form-control'}),
	'phone': forms.TextInput(attrs={'type': 'tel', 'class': 'form-control', 'minlength': 9, 'maxlength': 14}),
	'date_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
	'password': forms.PasswordInput(attrs={'type': 'password', 'class': 'form-control'})
}

class SignupForm(forms.ModelForm):
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
		widgets = WIDGETS
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

	def clean(self):
		cd = self.cleaned_data
		if self.errors:
			return cd
		email = self.cleaned_data.get('email')
		password = cd.get('password')
		password2 = cd.get('password2')
		terms = cd.get('terms')
		if get_user_model().objects.filter(email=email).exists():
			raise forms.ValidationError('Email already registered.')
		if not password:
			raise forms.ValidationError("Password can't be blank")
		if password != password2:
			raise forms.ValidationError("Passwords don't match")
		if len(password) < 4:
			raise forms.ValidationError("Password must be at least 4 characters long")
		if not terms:
			raise forms.ValidationError("You need accept the service terms.")
		return cd
	
	def __init__(self, *args, **kwargs):
		super(SignupForm, self).__init__(*args, **kwargs)


class UpdateForm(forms.ModelForm):
	class Meta:
		model = get_user_model()
		fields = ['first_name', 'last_name', 'email', 'cpf', 'phone', 'date_birth', 'password']
		labels = {
			'first_name': 'Nome',
			'last_name': 'Sobrenome',
			'email': 'E-mail',
			'cpf': 'CPF',
			'phone': 'Telefone',
			'date_birth': 'Data de nescimento',
			'password': _('Password')
		}
		widgets = WIDGETS
		help_texts = {
			'first_name': _('Name'),
			'last_name': _('Last name'),
			'email': 'E-mail',
			'cpf': 'CPF',
			'phone': _('Cell phone'),
			'date_birth': _('Date of birth'),
			'password': _('Password')
		}