from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create/', views.create, name='raffle_create'),
    # path('delete/', views.delete, name='raffle_delete'),
    path('update/', views.update, name='raffle_update'),
    path('list/', views.list, name='raffle_list'),
    path('<id>/', views.details, name='raffle_details'),
]
