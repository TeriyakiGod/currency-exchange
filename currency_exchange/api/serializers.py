from decimal import Decimal
from rest_framework import serializers
from .models import Currency, ExchangeRate


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ["code"]


class ExchangeRateSerializer(serializers.ModelSerializer):
    currency_pair = serializers.SerializerMethodField()
    exchange_rate = serializers.DecimalField(max_digits=10, decimal_places=6, min_value=Decimal("0.000001"), max_value=Decimal("999999999.999999"))

    class Meta:
        model = ExchangeRate
        fields = ["currency_pair", "exchange_rate"]

    def get_currency_pair(self, obj) -> str:
        return str(obj)

class ErrorSerializer(serializers.Serializer):
    error = serializers.CharField()