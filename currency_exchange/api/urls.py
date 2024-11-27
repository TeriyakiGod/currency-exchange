from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('currency/', views.currency_list, name='currency_list'),
    path('currency/<slug:base_currency>/<slug:quote_currency>/', views.exchange_rate, name='currency_exchange_rate'),
    path('currency/list', views.exchange_rate_list, name="exchange_rate_list")
]