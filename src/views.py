from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView
)
from rest_framework.response import Response
from .models import Raffle
from .serializer import RaffleSerializer


class RaffleListView(ListAPIView):
    queryset = Raffle.objects.all()
    serializer_class = RaffleSerializer

class RaffleDetailView(RetrieveAPIView):
    queryset = Raffle.objects.all()
    serializer_class = RaffleSerializer

class RaffleCreateView(CreateAPIView):
    queryset = Raffle.objects.all()
    serializer_class = RaffleSerializer

class RaffleUpdateView(UpdateAPIView):
    queryset = Raffle.objects.all()
    serializer_class = RaffleSerializer

class RaffleDeleteView(DestroyAPIView):
    queryset = Raffle.objects.all()
    serializer_class = RaffleSerializer
