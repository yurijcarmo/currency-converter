from django.urls import path
from .views import CurrencyList, ConvertCurrency

urlpatterns = [
    path('convert/', ConvertCurrency.as_view(), name='convert_currency_query'),
    path('currencies/', CurrencyList.as_view(), name='currency_list'),
]