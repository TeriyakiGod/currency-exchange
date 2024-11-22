from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from ..models import Currency, ExchangeRate
from typing import List
from django.utils import timezone


class TestCurrencyExchangeSetup(APITestCase):
    def setUp(self):
        # Create a test client
        self.client = APIClient()

        # Create a superuser
        self.superuser_username = "content_tester"
        self.superuser_password = "goldenstandard"
        self.superuser_email = "test@example.com"
        self.superuser = User.objects.create_superuser(
            self.superuser_username, self.superuser_email, self.superuser_password
        )

        # Create test currencies
        Currency.objects.create(code="USD")
        Currency.objects.create(code="EUR")
        Currency.objects.create(code="JPY")
        Currency.objects.create(code="PLN")

        self.currencies = Currency.objects.all().order_by("code")
        self.get_currency_expected_response = [
            {"code": currency.code} for currency in self.currencies
        ]

        # Create test exchange rates
        self.exchange_rates: List[ExchangeRate] = []
        self.test_rate = 1.0
        self.test_date = timezone.now()
        for currency in self.currencies:
            for target_currency in self.currencies:
                if currency != target_currency:
                    self.exchange_rates.append(
                        ExchangeRate.objects.create(
                            base_currency=currency,
                            target_currency=target_currency,
                            exchange_rate=self.test_rate,
                            datetime=self.test_date,
                        )
                    )

        self.get_exchange_rate_expected_responses = [
            {
                "currency_pair": f"{exchange_rate.base_currency.code}{exchange_rate.target_currency.code}",
                "exchange_rate": exchange_rate.exchange_rate,
            }
            for exchange_rate in self.exchange_rates
        ]
