from celery import shared_task
from .models import Cotacao
from datetime import datetime
from django.db.models import Max
from .data_fetcher import get_currency_data
import requests


def create_currency_instance(currency, response):
    return Cotacao(
        moeda=currency,
        data=datetime.strptime(response["date"], "%Y-%m-%d").date(),
        valor=response["rates"][currency]
    )


@shared_task
def fetch_new_data():
    latest_date = Cotacao.objects.aggregate(data_max=Max('data'))['data_max']

    if latest_date is None or datetime.now().date() > latest_date:
        response = get_currency_data(datetime.now().date())
        currencies = ["USD", "EUR", "JPY", "BRL"]

        new_currencies = [create_currency_instance(currency, response) for currency in currencies]

        Cotacao.objects.bulk_create(new_currencies)
        return "Os dados foram atualizados com sucesso"

    return "Os dados já estão atualizados"
