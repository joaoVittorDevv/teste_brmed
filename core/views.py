from django.shortcuts import render
from django.db.models import Sum, Q
from .models import Cotacao
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime
from decimal import Decimal
import json


class CustomJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.date):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)


def parse_date(request_date):
    return datetime.strptime(request_date, "%Y-%m-%d").date()


def get_grouped_values(currency, start_date, end_date):
    if currency == "ALL":
        annotations = {
            'usd': Sum('valor', filter=Q(moeda='USD')),
            'eur': Sum('valor', filter=Q(moeda='EUR')),
            'jpy': Sum('valor', filter=Q(moeda='JPY')),
            'brl': Sum('valor', filter=Q(moeda='BRL'))
        }
    else:
        annotations = {
            currency: Sum('valor', filter=Q(moeda=currency))
        }

    return Cotacao.objects.filter(
        moeda__in=['USD', 'EUR', 'JPY', 'BRL'],
        data__range=(start_date, end_date)
    ).values('data').annotate(**annotations).order_by('data')


def format_values_to_dictionary(values_grouped, currency):
    dictionaries = []
    for value in values_grouped:
        date = value['data'].strftime('%Y-%m-%d')
        if currency == "ALL":
            data_dict = {
                'data': date,
                'usd': float(value['usd']) if value['usd'] is not None else None,
                'eur': float(value['eur']) if value['eur'] is not None else None,
                'jpy': float(value['jpy']) if value['jpy'] is not None else None,
                'brl': float(value['brl']) if value['brl'] is not None else None
            }
        else:
            data_dict = {
                'data': date,
                currency.lower(): float(value.get(currency)) if value.get(currency) is not None else None
            }
        dictionaries.append(data_dict)
    return dictionaries



def cotacoes_view(request):
    if request.method == 'POST':
        end_date = parse_date(request.POST.get('end-date'))
        start_date = parse_date(request.POST.get('start-date'))
        currency = request.POST.get('currency')

        values_grouped = get_grouped_values(currency, start_date, end_date)
        dictionaries_list = format_values_to_dictionary(values_grouped, currency)

        return render(request, 'pages/home.html', {"data": json.dumps(dictionaries_list, cls=CustomJSONEncoder)})

    return render(request, 'pages/home.html')
