from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from core import settings
from .models import Raffle
from .forms import RaffleForm


@login_required(redirect_field_name='signin')
def dashboard(request):
    user = request.user
    if not user.is_authenticated:
        messages.warning(request, "Are you need to logged to exec the requisited page.")
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")
    context = {'raffles': False}
    if user.is_staff:
        context['raffles'] = Raffle.objects.filter(owner=user)
        return render(request, 'raffle/dashboard.html', context)
    return render(request, 'raffle/dashboard.html', context)

@login_required(redirect_field_name='signin')
def create(request):
    if request.method == 'POST':
        form = RaffleForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Your Raffle has been created succesfully!")
                return redirect('raffle_list')
            except:
                messages.warning(request, "Coudn't save, retry, please!")
    form = RaffleForm()
    return render(request, 'raffle/create.html', {'form': form})

@login_required(redirect_field_name='signin')
def delete(request, id):
    raffle = get_object_or_404(Raffle, id=id)
    if request.method == 'POST' and request.user.has_perm('delete_raffle'):
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

@login_required(redirect_field_name='signin')
def list(request):
    user = request.user
    raffles = Raffle.objects.filter(owner=user)
    return render(request, 'raffle/list.html', {'raffles': raffles})

@login_required(redirect_field_name='signin')
def details(request, id):
    user = request.user
    raffles = Raffle.objects.filter(owner=user)
    raffle = raffles.objects.get(id=id)
    return render(request, 'raffle/details.html', {'raffle': raffle})
