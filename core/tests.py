import unittest
from django.test import RequestFactory
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from .data_fetcher import fetch_data, get_last_thirty_days, get_currency_data
from .tasks import fetch_new_data, create_currency_instance
from .views import cotacoes_view, get_grouped_values, format_values_to_dictionary, parse_date


class TestViews(unittest.TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_parse_date(self):
        date_string = '2023-05-24'
        parsed_date = parse_date(date_string)

        self.assertEqual(parsed_date.year, 2023)
        self.assertEqual(parsed_date.month, 5)
        self.assertEqual(parsed_date.day, 24)

    @patch('core.models.Cotacao')
    def test_get_grouped_values(self, mock_cotacao):
        mock_cotacao.objects.filter.return_value.values.return_value.annotate.return_value.order_by.return_value = [{
            'data': parse_date('2023-05-24'),
            'usd': 1.2
        }]

        result = get_grouped_values('USD', parse_date('2023-05-24'), parse_date('2023-05-25'))

        self.assertEqual(len(result), 1)
        self.assertIn('USD', result[0])
        self.assertEqual(result[0]['USD'], 1.0)

    def test_format_values_to_dictionary(self):
        values_grouped = [{
            'data': parse_date('2023-05-24'),
            'usd': 1.2
        }]

        result = format_values_to_dictionary(values_grouped, 'USD')

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['data'], '2023-05-24')
        self.assertEqual(result[0]['usd'], None)

    @patch('core.views.get_grouped_values')
    @patch('core.views.format_values_to_dictionary')
    def test_cotacoes_view_post(self, mock_format_values_to_dictionary, mock_get_grouped_values):
        mock_get_grouped_values.return_value = []
        mock_format_values_to_dictionary.return_value = []

        request = self.factory.post('/cotacoes/', {
            'start-date': '2023-05-24',
            'end-date': '2023-05-25',
            'currency': 'USD'
        })

        response = cotacoes_view(request)

        self.assertEqual(response.status_code, 200)
        mock_get_grouped_values.assert_called_once()
        mock_format_values_to_dictionary.assert_called_once()

    def test_cotacoes_view_get(self):
        request = self.factory.get('/cotacoes/')

        response = cotacoes_view(request)

        self.assertEqual(response.status_code, 200)


class TestDataFetcher(unittest.TestCase):

    @patch('core.models.Cotacao')
    @patch('core.data_fetcher.get_currency_data')
    @patch('core.data_fetcher.get_last_thirty_days')
    def test_fetch_data(self, mock_get_last_thirty_days, mock_get_currency_data, mock_cotacao):
        mock_cotacao.objects.exists.return_value = False
        mock_get_last_thirty_days.return_value = [datetime.now().date()]
        mock_get_currency_data.return_value = {"rates": {"USD": 1.2, "EUR": 1.1, "JPY": 110.5, "BRL": 5.3}}

        fetch_data()

        self.assertEqual(mock_cotacao.objects.bulk_create.call_count, 1)
        calls = mock_cotacao.objects.bulk_create.call_args[0][0]
        self.assertEqual(len(calls), 4)

    def test_get_last_thirty_days(self):
        last_thirty_days = get_last_thirty_days()
        self.assertEqual(len(last_thirty_days), 30)

        for day in last_thirty_days:
            self.assertLess(day.weekday(), 5)

    @patch('requests.get')
    def test_get_currency_data(self, mock_get):
        date = datetime.now().date()
        mock_get.return_value.json.return_value = {"rates": {"USD": 1.2}}

        response = get_currency_data(date)

        mock_get.assert_called_once_with(f"https://api.vatcomply.com/rates?base=USD&date={date}")
        self.assertEqual(response["rates"]["USD"], 1.2)


class TestTasks(unittest.TestCase):

    @patch('core.models.Cotacao')
    @patch('core.tasks.get_currency_data')
    def test_fetch_new_data(self, mock_get_currency_data, mock_cotacao):
        mock_cotacao.objects.aggregate.return_value = {'data_max': datetime.now().date() - timedelta(days=1)}
        mock_get_currency_data.return_value = {
            "date": "2023-05-25",
            "rates": {"USD": 1.2, "EUR": 1.1, "JPY": 110.5, "BRL": 5.3}
        }

        result = fetch_new_data()

        self.assertEqual(mock_cotacao.objects.bulk_create.call_count, 1)
        calls = mock_cotacao.objects.bulk_create.call_args[0][0]
        self.assertEqual(len(calls), 4)
        self.assertEqual(calls[0].moeda, 'USD')
        self.assertEqual(result, 'Os dados foram atualizados com sucesso')

    @patch('core.models.Cotacao')
    @patch('core.tasks.get_currency_data')
    def test_fetch_new_data(self, mock_get_currency_data, mock_cotacao):
        mock_cotacao.objects.aggregate.return_value = {'data_max': datetime.now().date() - timedelta(days=2)}
        mock_get_currency_data.return_value = {
            "date": "2023-05-25",
            "rates": {"USD": 1.2, "EUR": 1.1, "JPY": 110.5, "BRL": 5.3}
        }

        result = fetch_new_data()

        self.assertEqual(mock_cotacao.objects.bulk_create.call_count, 0)
        self.assertEqual(result, 'Os dados já estão atualizados')

    @patch('core.models.Cotacao')
    def test_create_currency_instance(self, mock_cotacao):
        response = {"date": "2023-05-25", "rates": {"USD": 1.2}}
        currency = 'USD'

        instance = create_currency_instance(currency, response)

        self.assertEqual(instance.moeda, 'USD')
        self.assertEqual(instance.data, datetime.strptime(response["date"], "%Y-%m-%d").date())
        self.assertEqual(instance.valor, response["rates"][currency])


if __name__ == '__main__':
    unittest.main()

