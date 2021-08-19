from django.urls import path
from . import views

urlpatterns = [
    path('inventory', views.inventory, name='inventory'),
    path('login', views.login, name='login'),
    path('', views.inventory, name='home'),
    path('statistic', views.statistic, name='statistic'),
    path('delete/<int:pk>', views.item_delete, name='item-delete'),
    path('edit/<int:pk>', views.ItemUpdateView.as_view(), name='item-edit')
]
