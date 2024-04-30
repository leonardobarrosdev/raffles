from django.urls import path
from .views import (
    RaffleCreateView,
    RaffleDetailView,
    RaffleListView,
    RaffleUpdateView,
    RaffleDeleteView
)

urlpatterns = [
    path('raffles/', RaffleCreateView.as_view(), name='raffle-list'),
    path('raffle/{pk}/detail/', RaffleDetailView.as_view(), name='raffle-detail'),
    path('raffle/create/', RaffleListView.as_view(), name='raffle-create'),
    path('raffle/{pk}/update/', RaffleUpdateView.as_view(), name='raffle-update'),
    path('raffle/[pk]/delete/', RaffleDeleteView.as_view(), name='raffle-delete')
]
