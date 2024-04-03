import decimal
import requests
import logging
from datetime import timedelta
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .models import Currency
from .serializers import CurrencySerializer
from decouple import config

API_KEY = config('API_KEY')

logger = logging.getLogger(__name__)

FIAT_CURRENCY_API_URL = f'https://api.fastforex.io/fetch-all?from=usd&api_key={API_KEY}'
CRYPTO_CURRENCY_API_URL = f'https://api.fastforex.io/crypto/fetch-prices?pairs=BTC%2FUSD%2CETH%2FUSD&api_key={API_KEY}'
UPDATE_INTERVAL_IN_HOURS = 1  # hours

class ConvertCurrency(APIView):
    def get(self, request):
        from_currency = request.query_params.get('from')
        to_currency = request.query_params.get('to')
        amount = request.query_params.get('amount')

        try:
            self.update_rates_if_necessary()
            return self.perform_conversion(from_currency, to_currency, amount)

        except Exception as e:
            logger.error(str(e))
            return Response(
                {'error': 'Unexpected error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def update_rates_if_necessary(self):
        last_updated = None
        try:
            last_updated = Currency.objects.latest('updated_at')
        except Currency.DoesNotExist:
            pass

        if not last_updated or \
                last_updated.updated_at < \
                timezone.now() - timedelta(hours=UPDATE_INTERVAL_IN_HOURS):
            self.update_rates()

    def update_rates(self):
        response = requests.get(FIAT_CURRENCY_API_URL)
        exchangeRateResponse = response.json()

        if 'results' not in exchangeRateResponse:
            raise Exception('Could not fetch rates')

        for code, rate in exchangeRateResponse['results'].items():
            Currency.objects.update_or_create(
                code=code,
                defaults={'rate': rate}
            )

        response = requests.get(CRYPTO_CURRENCY_API_URL)
        cryptoResponse = response.json()

        if 'prices' not in cryptoResponse:
            raise Exception('Could not fetch rates')

        for code, rate in cryptoResponse['prices'].items():
            code = 'BTC' if code == 'BTC/USD' else 'ETH'
            Currency.objects.update_or_create(
                code=code,
                defaults={'rate': rate}
            )

    def perform_conversion(self, from_currency, to_currency, amount):
        
        decimal.getcontext().prec = 10
        try:
            amount_decimal = decimal.Decimal(amount)
        except decimal.InvalidOperation:
            return Response(
                {'error': 'Invalid amount value'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            from_rate = Currency.objects.get(code=from_currency.upper()).rate
            to_rate = Currency.objects.get(code=to_currency.upper()).rate
        except (Currency.DoesNotExist):
            return Response(
                {'error': 'Invalid input data'},
                status=status.HTTP_400_BAD_REQUEST
            )

        prec_from_rate = decimal.Decimal(from_rate)
        prec_to_rate = decimal.Decimal(to_rate)

        try:
            usd_amount = amount_decimal * prec_from_rate
            converted_amount = usd_amount * prec_to_rate
        except decimal.DecimalException:
            return Response(
                {'error': 'Error performing conversion'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response({'converted_amount': '{:.2f} {}'.format(converted_amount, to_currency)})

class CurrencyList(generics.ListAPIView):
    convert_currency_instance = ConvertCurrency()
    convert_currency_instance.update_rates_if_necessary()

    """ For getting all currencies """
    queryset = Currency.objects.all().order_by('code')
    serializer_class = CurrencySerializer
