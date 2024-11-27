from django.shortcuts import redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Currency, ExchangeRate
from .serializers import CurrencySerializer, ExchangeRateSerializer, ErrorSerializer
from drf_spectacular.utils import extend_schema
from django_filters import rest_framework as filters

class ExchangeRateFilter(filters.FilterSet):
    base_currency = filters.CharFilter(field_name="base_currency__code", lookup_expr="iexact")
    target_currency = filters.CharFilter(field_name="target_currency__code", lookup_expr="iexact")

    class Meta:
        model = ExchangeRate
        fields = ['base_currency__code', 'target_currency__code']


def index(_):
    return redirect("swagger")


@extend_schema(
    responses=CurrencySerializer(many=True),
    description="List all currencies stored in the database",
)
@api_view(["GET"])
def currency_list(request):
    currencies = Currency.objects.all().order_by("code")
    serializer = CurrencySerializer(currencies, many=True)
    return Response(serializer.data)


@extend_schema(
    responses={
        200: ExchangeRateSerializer,
        400: ErrorSerializer,
        404: ErrorSerializer,
    },
    description="Get the latest exchange rate between two currencies",
)
@api_view(["GET"])
def exchange_rate(request, base_currency, quote_currency):
    try:
        base_currency = Currency.objects.get(code=base_currency)
    except Currency.DoesNotExist:
        serializer = ErrorSerializer({"error": f"Currency {base_currency} not found"})
        return Response(serializer.data, status=404)
    try:
        quote_currency = Currency.objects.get(code=quote_currency)
    except Currency.DoesNotExist:
        serializer = ErrorSerializer({"error": f"Currency {quote_currency} not found"})
        return Response(serializer.data, status=404)
    if base_currency == quote_currency:
        serializer = ErrorSerializer(
            {"error": "Base currency and quote currency cannot be the same"}
        )
        return Response(serializer.data, status=400)
    exchange_rate = (
        ExchangeRate.objects.filter(
            base_currency=base_currency, target_currency=quote_currency
        )
        .order_by("-datetime")
        .first()
    )
    serializer = ExchangeRateSerializer(exchange_rate)
    return Response(serializer.data)

@api_view(["GET"])
def exchange_rate_list(request):
    f = ExchangeRateFilter(request.GET, queryset=ExchangeRate.objects.all())
    serializer = ExchangeRateSerializer(f.qs, many=True)
    return Response(serializer.data)