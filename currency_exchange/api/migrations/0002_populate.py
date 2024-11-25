from django.db import migrations
import os
from django.core.management import call_command

def populate_currencies(apps, schema_editor):
    default_currencies = os.environ.get('DEFAULT_CURRENCIES', 'USD,EUR,JPY,PLN').split(',')
    Currency = apps.get_model('api', 'Currency')
    for currency in default_currencies:
        Currency.objects.create(code=currency)


def populate_exchange_rates(apps, schema_editor):
    call_command('fetch_latest_rates')


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_currencies),
        migrations.RunPython(populate_exchange_rates),
    ]
