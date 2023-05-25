import requests
from datetime import datetime, timedelta


def fetch_data():
    from .models import Cotacao

    if Cotacao.objects.exists():
        return

    last_thirty_work_days = get_last_thirty_days()
    all_currency = []

    for date in last_thirty_work_days:
        response = get_currency_data(date)

        all_currency.extend(
            [
                Cotacao(moeda="USD", data=date, valor=response["rates"]["USD"]),
                Cotacao(moeda="EUR", data=date, valor=response["rates"]["EUR"]),
                Cotacao(moeda="JPY", data=date, valor=response["rates"]["JPY"]),
                Cotacao(moeda="BRL", data=date, valor=response["rates"]["BRL"]),
            ]
        )

    Cotacao.objects.bulk_create(all_currency)


def get_last_thirty_days():
    current_date = datetime.now()
    last_thirty_work_days = []
    work_day_counter = 0

    while work_day_counter < 30:
        current_date -= timedelta(days=1)
        if current_date.weekday() < 5:
            last_thirty_work_days.append(current_date.date())
            work_day_counter += 1

    last_thirty_work_days.reverse()
    return last_thirty_work_days


def get_currency_data(date):
    response = requests.get(f"https://api.vatcomply.com/rates?base=USD&date={date}").json()
    return response

