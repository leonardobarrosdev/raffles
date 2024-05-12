from django.urls import include, path
from rest_framework import routers
from .views import RaffleViewSet

router = routers.SimpleRouter()
router.register(r'raffles/', RaffleViewSet, basename='raffle')
urlpatterns = router.urls
