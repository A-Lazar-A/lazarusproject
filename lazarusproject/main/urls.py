from django.urls import path
from . import views

urlpatterns = [
    path('inventory', views.inventory, name='inventory'),
    path('login', views.login, name='login'),
    path('', views.inventory, name='home'),
    path('statistic', views.statistic, name='statistic'),
]
