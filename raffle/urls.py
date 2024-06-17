from django.urls import path
from . import views

urlpatterns = [
	path('list/', views.list, name='raffle_list'),
	path('create/', views.CreateView.as_view(), name='raffle_create'),
	path('<int:id>/', views.details, name='raffle_details'),
	path('update/<int:id>/', views.UpdateView.as_view(), name='raffle_update'),
	path('delete/<int:id>/', views.delete, name='raffle_delete'),
]
