from .test_setup import TestCurrencyExchangeSetup
from ..models import Currency, ExchangeRate

class TestCurrencyExchangeModels(TestCurrencyExchangeSetup):
    def test_currency_creation(self):
        # Test that all currencies were created
        self.assertEqual(Currency.objects.count(), 4)

        # Test attributes of a single currency
        usd = Currency.objects.get(code="USD")
        self.assertEqual(usd.name, "United States Dollar")
        self.assertEqual(usd.code, "USD")

    def test_currency_get_rates(self):
        # Test that each currency has exactly 3 rates (since there are 4 currencies total)
        for currency in self.currencies:
            rates = currency.get_rates()
            self.assertEqual(len(rates), 3)

    def test_exchange_rate_creation(self):
        # Test that all exchange rates were created
        total_exchange_rates = len(self.currencies) * (len(self.currencies) - 1)
        self.assertEqual(ExchangeRate.objects.count(), total_exchange_rates)

    def test_currency_str(self):
        # Test the __str__ method of the Currency model
        usd = Currency.objects.get(code="USD")
        self.assertEqual(str(usd), "USD")
    
    def test_exchange_rate_str(self):
        # Test the __str__ method of the ExchangeRate model
        exchange_rate = ExchangeRate.objects.first()
        self.assertEqual(str(exchange_rate), f"{exchange_rate.base_currency.code}{exchange_rate.target_currency.code}")