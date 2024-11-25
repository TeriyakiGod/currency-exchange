from .test_setup import TestCurrencyExchangeSetup
from ..models import Currency, ExchangeRate

class ExchangeRateModelAdminTests(TestCurrencyExchangeSetup):
    def test_update_exchange_rates(self):
        """
        This tests the update_exchange_rates method in the ExchangeRateAdmin class.
        The method should fetch current (at the time of execution) exchange rates for all currency combinations.
        """
        # Empty exchange rates for testing purposes
        ExchangeRate.objects.all().delete()
        # Check if setup is correct
        self.assertEqual(ExchangeRate.objects.count(), 0)
        self.assertEqual(Currency.objects.count(), 4)
        # Login as superuser
        self.apiclient.login(username=self.superuser_username, password=self.superuser_password)
        # Call the update_exchange_rates
        response = self.apiclient.get('/admin/api/exchangerate/update/')
        self.assertEqual(response.status_code, 302)
        # Check if exchange rates were created
        self.assertEqual(ExchangeRate.objects.count(), 12)
        # Check if there is 3 rates for each currency
        for currency in Currency.objects.all():
            self.assertEqual(currency.get_rates().count(), 3)
        