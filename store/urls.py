from django.urls import path, re_path
from . import views

app_name = 'store'

urlpatterns = [
	path('', views.store, name='index'),
	path('cart/', views.cart, name='cart'),
	path('checkout/', views.CheckoutView.as_view(), name='checkout'),
	path('add-subitems/', views.add_subitems, name="add-subitems"),
]
