from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import settings
from apps.product.models import Product


def is_admin(user):
	return user.groups.filter(name='ADMIN').exists()

@login_required(redirect_field_name='signin')
def dashboard(request):
	user = request.user
	if not user.is_authenticated:
		messages.warning(request, "Are you need to logged to exec the requisited page.")
		return redirect(f"{settings.LOGIN_URL}?next={request.path}")
	context = {'products': False}
	if user.is_staff:
		context['products'] = Product.objects.filter(owner=user)
		return render(request, 'admin/dashboard.html', context)
	return render(request, 'admin/dashboard.html', context)
