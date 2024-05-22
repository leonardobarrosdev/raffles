from django.shortcuts import render, redirect, resolve_url
from .models import Raffle


def dashboard(request):
    return render(request, 'raffle/dashboard.html')
def create(request):
    return render(request, 'raffle/create.html')
# def delete(request):
#     return render(request, 'raffle/')
def update(request):
    return render(request, 'raffle/update.html')
def list(request):
    return render(request, 'raffle/list.html')
def details(request, id):
    return render(request, 'raffle/details.html')
