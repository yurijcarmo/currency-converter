from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch
from .models import Currency
from .views import ConvertCurrency

class ConvertCurrencyTestCase(TestCase):
    @patch('requests.get')
    def test_perform_conversion(self, mock_get):
        Currency.objects.create(code='USD', rate=1.0)
        Currency.objects.create(code='EUR', rate=0.8)

        response = ConvertCurrency().perform_conversion('USD', 'EUR', '100')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['converted_amount'], '80.00 EUR')

        response = ConvertCurrency().perform_conversion('ABC', 'EUR', '100')
        self.assertEqual(response.status_code, 400)

        response = ConvertCurrency().perform_conversion('USD', 'EUR', 'abc')
        self.assertEqual(response.status_code, 400)

    def test_currency_list(self):
        response = self.client.get(reverse('currency_list'))
        self.assertEqual(response.status_code, 200)

class CurrencyModelTestCase(TestCase):
    def test_create_currency(self):
        currency = Currency.objects.create(code='USD', rate=1.0)
        self.assertEqual(currency.code, 'USD')
        self.assertEqual(currency.rate, 1.0)

    def test_currency_updated_at(self):
        currency = Currency.objects.create(code='USD', rate=1.0)
        initial_updated_at = currency.updated_at

        currency.rate = 1.1
        currency.save()

        updated_currency = Currency.objects.get(id=currency.id)

        self.assertNotEqual(initial_updated_at, updated_currency.updated_at)