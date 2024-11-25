from django.core.management.base import BaseCommand, CommandError
from ...models import Currency, ExchangeRate
from yfinance import Ticker


class Command(BaseCommand):
    help = "Fetches latest exchange rates for all currency pairs and saves them to the database"

    def handle(self, *args, **options):
        if Currency.objects.count() < 2:
            raise CommandError("Need at least two currencies to update exchange rates")
        currencies = Currency.objects.all()
        for base_currency in currencies:
            for target_currency in currencies:
                if base_currency != target_currency:
                    try:
                        current_exchange_rate = Ticker(
                            f"{base_currency.code}{target_currency.code}=X"
                        ).fast_info["last_price"]
                    except KeyError:
                        self.stdout.write(
                            self.style.ERROR(
                                f"Failed to fetch exchange rate for {base_currency.code}{target_currency.code}"
                            )
                        )
                        continue
                    ExchangeRate.objects.create(
                        base_currency=base_currency,
                        target_currency=target_currency,
                        exchange_rate=current_exchange_rate,
                    )
        self.stdout.write(self.style.SUCCESS("Successfully updated exchange rates"))
