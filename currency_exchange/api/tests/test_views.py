from .test_setup import TestCurrencyExchangeSetup


class TestCurrencyExchangeViews(TestCurrencyExchangeSetup):
    def test_get_currency(self):
        response = self.client.get("/currency/")
        # Ensure the response status code is 200
        self.assertEqual(response.status_code, 200)
        
        # Ensure the response is JSON
        self.assertEqual(response.content_type, "application/json")
        
        # Parse the JSON response
        response_data = response.json()
        
        # Check the response length
        self.assertEqual(len(response_data), len(self.get_currency_expected_response))
        
        # Compare with expected response
        self.assertEqual(response_data, self.get_currency_expected_response)

    def test_get_exchange_rate(self):
        for exchange_rate, expected_response in zip(
            self.exchange_rates, self.get_exchange_rate_expected_responses
        ):
            response = self.client.get(
                f"/exchange_rate/{exchange_rate.base_currency.code}/{exchange_rate.target_currency.code}/"
            )
            # Ensure the response status code is 200
            self.assertEqual(response.status_code, 200)
            
            # Ensure the response is JSON
            self.assertEqual(response.content_type, "application/json")
            
            # Parse the JSON response
            response_data = response.json()
            
            # Compare with the expected response
            self.assertEqual(response_data, expected_response)
