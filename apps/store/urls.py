from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
	path('', views.store, name='home'),
	path('cart/', views.cart, name='cart'),
	path('checkout/', views.CheckoutView.as_view(), name='checkout'),
	path('add-subitems/<int:product_id>/', views.add_subitems, name="add-subitems"),
]
