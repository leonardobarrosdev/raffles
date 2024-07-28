from django.urls import path, re_path
from . import views

app_name = 'raffle'

urlpatterns = [
	path('raffles/', views.list, name='list'),
	re_path(r'^(?P<id>[0-9])?/$', views.RaffleView.as_view(), name='raffle')
]
