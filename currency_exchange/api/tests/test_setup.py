from rest_framework.test import APITestCase, APIClient
from ..models import Currency, ExchangeRate
import random


class TestCurrencyExchangeSetup(APITestCase):
    def setUp(self):
        # Create a test client
        self.client = APIClient()

        # Seed for reproducibility
        random.seed(42)

        # Create test currencies
        self.usd = Currency.objects.create(code="USD", name="United States Dollar")
        self.eur = Currency.objects.create(code="EUR", name="Euro")
        self.jpy = Currency.objects.create(code="JPY", name="Japanese Yen")
        self.pln = Currency.objects.create(code="PLN", name="Polish Zloty")

        self.currencies = Currency.objects.all()

        # Create exchange rates
        self.create_exchange_rates()

        # Prepare expected responses
        self.get_currency_expected_response = [
            {"code": currency.code} for currency in self.currencies
        ]

        self.get_exchange_rate_expected_responses = [
            {
                "currency_pair": f"{exchange_rate.base_currency.code}{exchange_rate.target_currency.code}",
                "exchange_rate": f"{exchange_rate.rate:.2f}",
            }
            for exchange_rate in self.exchange_rates
        ]

    def create_exchange_rates(self):
        for base_currency in self.currencies:
            for target_currency in self.currencies:
                if base_currency != target_currency:
                    ExchangeRate.objects.create(
                        base_currency=base_currency,
                        target_currency=target_currency,
                        rate=random.uniform(0.5, 1.5),  # Realistic range
                        date="2021-01-01",
                    )
        self.exchange_rates = ExchangeRate.objects.all()
