from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('currency/', views.currency_list, name='currency_list'),
    path('currency/<str:base_currency>/<str:target_currency>/', views.exchange_rate, name='currency_exchange_rate'),
]