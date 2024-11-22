from django.shortcuts import redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Currency, ExchangeRate
from .serializers import CurrencySerializer, ExchangeRateSerializer, ErrorSerializer
from drf_spectacular.utils import extend_schema
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.openapi import OpenApiParameter


def index(_):
    return redirect("swagger")


@extend_schema(responses=CurrencySerializer(many=True))
@api_view(["GET"])
def currency_list(request):
    currencies = Currency.objects.all().order_by("code")
    serializer = CurrencySerializer(currencies, many=True)
    return Response(serializer.data)


@extend_schema(
    parameters=[
        OpenApiParameter(
            name="base_currency",
            type=OpenApiTypes.STR,
            description="Base currency code",
            enum=[currency.code for currency in Currency.objects.all()],
            location=OpenApiParameter.PATH,
        ),
        OpenApiParameter(
            name="target_currency",
            type=OpenApiTypes.STR,
            description="Target currency code",
            enum=[currency.code for currency in Currency.objects.all()],
            location=OpenApiParameter.PATH,
        ),
    ],
    responses={
        200: ExchangeRateSerializer,
        400: ErrorSerializer,
        404: ErrorSerializer,
    },
)
@api_view(["GET"])
def exchange_rate(request, base_currency, target_currency):
    try:
        base_currency = Currency.objects.get(code=base_currency)
    except Currency.DoesNotExist:
        return Response({"error": f"Currency {base_currency} not found"}, status=404)
    try:
        target_currency = Currency.objects.get(code=target_currency)
    except Currency.DoesNotExist:
        return Response({"error": f"Currency {target_currency} not found"}, status=404)
    if base_currency == target_currency:
        return Response(
            {"error": "Base and target currencies are the same"}, status=400
        )
    exchange_rate = ExchangeRate.objects.filter(
        base_currency=base_currency, target_currency=target_currency
    ).order_by('-datetime').first()
    serializer = ExchangeRateSerializer(exchange_rate)
    return Response(serializer.data)
