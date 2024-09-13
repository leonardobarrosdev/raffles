from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
from django.views.generic.base import View
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from core import settings
from .utils import AppTokenGenerator
from .forms import SignupForm, UpdateForm
import ipdb


class SignupView(View):
	User = get_user_model()
	template_name = 'user/signup.html'

	def get(self, request):
		if request.user.is_authenticated:
			return redirect('store:home')
		context = {'form': SignupForm()}
		return render(request, self.template_name, context)

	def post(self, request):
		form = SignupForm(request.POST)
		if form.is_valid():
			form.cleaned_data['email']
			form.cleaned_data['password2']
			form.cleaned_data['terms']
			user = form.save(commit=False)
			user.is_active = False
			user.save()
			send_email_welcome(user.first_name, user.email)
			_send_confirm_email(request, user)
			messages.success(request, "Your account has been created succesfully! Please check your email address in order to activate your account.")
			return redirect('user:signin')
		return render(request, self.template_name, {'form': form})


def send_email_welcome(first_name, email):
	subject = "Welcome to your Website from Raffles!"
	message = f"Hello {first_name}, welcome to us platform. We are send this message for that you confirm you account."
	from_email = settings.EMAIL_HOST_USER
	send_mail(subject, message, from_email, [email], fail_silently=True)

def _send_confirm_email(request, user):
	generate_token = AppTokenGenerator()
	current_site = get_current_site(request)
	subject = "Confirm your Email🔑"
	message = render_to_string('user/email_confirmation.html', {
		'name': user.first_name,
		'domain': current_site.domain,
		'uid': urlsafe_base64_encode(force_bytes(user.id)),
		'token': generate_token.make_token(user),
		'protocol': 'https' if request.is_secure() else 'http',
		'activate_url': reverse('user:activate', kwargs={
            'uidb64': urlsafe_base64_encode(force_bytes(user.id)),
            'token': generate_token.make_token(user)
        })
	})
	from_email = settings.EMAIL_HOST_USER
	email = EmailMessage(subject, message, from_email, [user.email])
	email.send()

def activate(request, uidb64, token):
	User = get_user_model()
	generate_token = AppTokenGenerator()
	try:
		uid = force_str(urlsafe_base64_decode(uidb64))
		user = User.objects.get(id=uid)
	except (TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None
	if user is not None and generate_token.check_token(user, token):
		user.is_active = True
		user.save()
		messages.success(request, "Your Account has been activated!")
		return redirect('user:signin')
	messages.error(request, "Activation link is invalid!")
	return render(request, 'user/signup.html', {'form': SignupForm()})

def signin(request):
	if request.user.is_authenticated:
		return redirect('store:home')
	if not request.user.is_active:
		messages.error(request, "Your account is not activated yet.")
		return redirect('user:signin')
	if request.method == 'POST':
		email = request.POST['email']
		password = request.POST['password']
		user = authenticate(request, email=email, password=password)
		if user is not None:
			login(request, user)
			return redirect(request.POST.get('next', "store:home"))
	messages.error(request, "Bad Credentials.")
	return render(request, 'user/signin.html')

def signout(request):
	logout(request)
	return redirect('store:home')


class UpdateDetailsView(View):
	User = get_user_model()
	template_name = 'user/update_details.html'

	def get(self, request, id):
		user = get_object_or_404(self.User, id=id)
		form = UpdateForm(instance=user)
		context = {'form': form, 'user': user}
		return render(request, self.template_name, context)

	def post(self, request, id):
		user = get_object_or_404(self.User, id=id)
		form = UpdateForm(request.POST, instance=user)
		if form.is_valid():
			form.save()
			messages.success(request, "Update succesfully realized!")
			return redirect('user:update_details', id=id)
		return render(request, self.template_name, {'form': form, 'user': user})