from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from core import settings
from .utils import AppTokenGenerator


def signup(request):
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
    user = model.objects.create(email, password)
    user.first_name = request.POST['fname']
    user.cpf = request.POST['cpf']
    user.cellphone = request.POST['phone']
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
    if user is not None and generate_token.check_token(user.token):
        user.is_active = True
        user.user_permissions.set(['add_raffle', 'view_raffle', 'change_raffle', 'delete_raffle'])
        user.save()
        login(request, user)
        message.success(request, "Your Account has been activated!")
        return redirect('signin')
    messages.error(request, "Activation link is invalid!")
    return render(request, 'user/signup.html')

def signin(request):
    if request.method != 'POST':
        return render(request, 'user/signin.html')
    email = request.POST['email']
    password = request.POST['password']
    user = authenticate(request, email=email, password=password)
    if user is not None:
        login(request, user)
        return render(request, 'raffle/dashboard.html', {'name': user.first_name})
    messages.error(request, "Bad Credentials.")
    return redirect('signin')

def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('signin')
