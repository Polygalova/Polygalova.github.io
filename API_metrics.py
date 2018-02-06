import requests
import datetime


class YandexMetricsUser:
    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            'Authorization': 'OAuth {}'.format(self.token),
            'Content-Type': 'application/json'}

    def get_counter_list(self):
        headers = self.get_headers()
        response = requests.get('https://api-metrika.yandex.ru/management/v1/counters', headers=headers)
        counters = response.json()['counters']
        return [counter['id'] for counter in counters]


class YandexMetricsCounter(YandexMetricsUser):

    def __init__(self, token, counter_id):
        super().__init__(token)
        self.counter_id = counter_id

    def get_counter_metrics(self):
        headers = self.get_headers()
        params = {
            'pretty': 1,
            'direct_client_logins': 'yndx.polygalova',
            'ids': self.counter_id,
            'metrics': 'ym:s:visits, ym:s:pageviews, ym:s:users',
            'date1': datetime.date.today(),
            'date2': datetime.date.today()
        }
        response = requests.get('https://api-metrika.yandex.ru/stat/v1/data', headers=headers, params=params)
        result = response.json()['totals']
        print('Сегодня на сайте с номером счетчика {} визитов: {}, просмотров: {}, посетителей: {}.'
              .format(self.counter_id, *result))


my_token = 'AQAAAAAb6BgaAATL8G_paSMnlk3Nkq17zKft2kQ'
Larisa = YandexMetricsUser(my_token)
my_counters = Larisa.get_counter_list()
for counter in my_counters:
    my_counter = YandexMetricsCounter(Larisa.token, counter)
    my_counter.get_counter_metrics()
