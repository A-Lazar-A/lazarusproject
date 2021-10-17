from django.urls import path
from . import views

urlpatterns = [
    # path('inventory/', views.ItemCreateView.as_view(), name='inventory'),
    path('inventory/', views.MainTemplateView.as_view(), name='inventory'),
    path('create', views.ItemFormView.as_view(), name='item-create'),
    path('login', views.UserLoginView.as_view(), name='login'),
    path('logout', views.UserLogoutView.as_view(), name='logout'),
    path('sign-up', views.UserRegisterView.as_view(), name='sign-up'),
    path('', views.UserLoginView.as_view(), name='home'),
    path('statistic', views.StatisticView.as_view(), name='statistic'),
    path('delete/<int:pk>', views.ItemDeleteView.as_view(), name='item-delete'),
    path('edit/<int:pk>', views.ItemUpdateView.as_view(), name='item-edit'),
    path('meeting-create/<int:pk>', views.MeetingsFormView.as_view(), name='meeting-create'),
    path('meeting-add/<int:pk>', views.AddItemForMeetingFormView.as_view(), name='meeting-add'),
    path('meeting-done/<int:pk>', views.GoodMeetingDeleteView.as_view(), name='meeting-done'),
    path('meeting-delete/<int:pk>', views.MeetingDeleteView.as_view(), name='meeting-delete'),
    path('delivery', views.DeliveryView.as_view(), name='delivery'),
    path('meetings', views.MeetingsListView.as_view(), name='meetings')
]
