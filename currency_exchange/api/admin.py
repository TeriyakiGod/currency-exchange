from django.contrib import admin
from django.urls import path
from .models import Currency, ExchangeRate
from yfinance import Ticker
from django.shortcuts import redirect


@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    change_list_template = "admin/exchangerate_changelist.html"
    list_display = [
        "currency_pair",
        "rate",
        "datetime",
    ]
    readonly_fields = ["datetime"]
    ordering = ["-datetime"]

    def currency_pair(self, obj):
        return str(obj)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("update/", self.update_exchange_rates, name="update"),
        ]
        return custom_urls + urls

    def update_exchange_rates(self, request):
        """
        Fetches the current exchange rates for all currency combinations and saves them to the database. (dont override old rates)
        """
        if Currency.objects.count() < 2:
            self.message_user(
                request, "Need at least two currencies to update exchange rates"
            )
            return redirect("..")
        currencies = Currency.objects.all()
        for base_currency in currencies:
            for target_currency in currencies:
                if base_currency != target_currency:
                    try:
                        current_exchange_rate = Ticker(
                            f"{base_currency.code}{target_currency.code}=X"
                        ).fast_info["last_price"]
                    except KeyError:
                        self.message_user(
                            request,
                            f"Failed to fetch exchange rate for {base_currency.code}{target_currency.code}",
                        )
                        continue
                    ExchangeRate.objects.create(
                        base_currency=base_currency,
                        target_currency=target_currency,
                        rate=current_exchange_rate,
                    )
        self.message_user(request, "Exchange rates updated")
        return redirect("..")


admin.site.register(Currency)
