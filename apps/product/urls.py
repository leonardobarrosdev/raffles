from django.urls import path, re_path
from . import views

app_name = 'product'

urlpatterns = [
	path('list/', views.product_list, name='list'),
	path('create/', views.ProductCreateView.as_view(), name='create'),
	path('<int:id>/', views.product_details, name='details'),
	path('<int:id>/delete/', views.product_delete, name='delete'),
]
