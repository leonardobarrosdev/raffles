from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAdminUser
from rest_framework import viewsets
from rest_framework.response import Response
from .models import UserProfile
from .serializer import CustomerSerializer, OwnerSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = CustomerSerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class OwnerViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()

    def list(self, request):
        serializer = OwnerSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        owner = get_object_or_404(self.queryset, pk=pk)
        serializer = OwnerSerializer(owner)
        return Response(serializer.data)

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy'):
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
