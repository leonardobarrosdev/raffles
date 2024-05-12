from rest_framework import routers
from .views import CustomerViewSet, OwnerViewSet

router = routers.SimpleRouter()
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'owners', OwnerViewSet, basename='owner')
urlpatterns = router.urls
