from django.urls import path
from . import views

urlpatterns = [
    path('inventory/', views.ItemCreateView.as_view(), name='inventory'),
    path('login', views.UserLoginView.as_view(), name='login'),
    path('logout', views.UserLogoutView.as_view(), name='logout'),
    path('sign-up', views.UserRegisterView.as_view(), name='sign-up'),
    path('', views.UserLoginView.as_view(), name='home'),
    path('statistic', views.statistic, name='statistic'),
    path('delete/<int:pk>', views.ItemDeleteView.as_view(), name='item-delete'),
    path('edit/<int:pk>', views.ItemUpdateView.as_view(), name='item-edit'),
    path('meeting-create/<int:pk>', views.MeetingCreateView.as_view(), name='meeting-create'),
    path('delivery', views.DeliveryView.as_view(), name='delivery')
]
