from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from .models import Raffle
from .serializer import RaffleSerializer


class RaffleViewSet(viewsets.ModelViewSet):
    queryset = Raffle.objects.all()
    serializer_class = RaffleSerializer

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
