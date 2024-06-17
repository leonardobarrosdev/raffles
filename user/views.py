from tokenize import generate_tokens
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from core import settings
from .utils import AppTokenGenerator
from .forms import UserProfileForm


def signup(request):
	if request.user.is_authenticated:
		return redirect('store')
	if request.method != 'POST':
		return render(request, 'user/signup.html')
	model = get_user_model()
	email = request.POST['email']
	password = request.POST['password']
	password2 = request.POST['password2']
	if model.objects.filter(email=email).exists():
		messages.error(request, "Email already registered.")
		return redirect('signup')
	if password != password2:
		messages.error(request, "Password didn't matched.")
		return redirect('signup')
	user = model.objects.create_customer(email, password)
	user.first_name = request.POST['fname']
	user.cpf = request.POST['cpf']
	user.phone = request.POST['phone']
	user.date_birth = request.POST['date_birth']
	user.is_active = False
	user.save()
	messages.success(request, "Your account has been created succesfully! Please check your email address in order to activate your account.")
	send_email_welcome(user.first_name, email)
	_send_confirm_email(request, user)
	return redirect('signin')

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
		'protocol': 'https' if request.is_secure() else 'http'
	})
	from_email = settings.EMAIL_HOST_USER
	email = EmailMessage(subject, message, from_email, [user.email])
	send_mail(subject, message, from_email, [user.email], fail_silently=True)

def activate(request, uidb64, token):
	model = get_user_model()
	try:
		uid = force_str(urlsafe_base64_decode(uidb64))
		user = model.objects.get(id=uid)
	except (TypeError, ValueError, OverflowError, model.DoesNotExist):
		user = None
	if user is not None and generate_tokens.check_token(user.token):
		user.is_active = True
		user.user_permissions.set(['add_raffle', 'view_raffle', 'change_raffle', 'delete_raffle'])
		user.save()
		login(request, user)
		messages.success(request, "Your Account has been activated!")
		return redirect('signin')
	messages.error(request, "Activation link is invalid!")
	return render(request, 'user/signup.html')

def signin(request):
	if request.user.is_authenticated:
		return redirect('store')
	if request.method == 'POST':
		email = request.POST['email']
		password = request.POST['password']
		user = {'email': email, 'password': password}
		user = authenticate(request, email=email, password=password)
		if user is not None:
			login(request, user)
			if not user.is_staff:
				return redirect("store")
			return render(request, 'admin/dashboard.html', {'user': user})
	messages.error(request, "Bad Credentials.")
	return render(request, 'user/signin.html')

def signout(request):
	logout(request)
	return redirect('store')

def update_details(request, id):
	user_model = get_user_model()
	user = get_object_or_404(user_model, id=id)
	form = UserProfileForm(request.POST or None, instance=user)
	context = {'form': form, 'user': user}
	if request.method == 'POST' and form.is_valid():
		try:
			form.save()
			messages.success(request, "Update succesfully realized!")
			redirect('user_update_details')
		except Exception as e:
			print("Update is ", e)
	return render(request, 'user/update_details.html', context)
