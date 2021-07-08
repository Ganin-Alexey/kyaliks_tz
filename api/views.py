from django.conf import settings
from django.views import View
from django.http import HttpResponse
import requests
import json


class AuthAPI(View):
    def get(self, request, method_name='auth.check'):
        headers = {'content-type': 'application/json'}
        payload = {
            "method": method_name,
            "params": {},
            "jsonrpc": "2.0",
            "id": 0,
        }
        # Validate data
        try:
            response = requests.post('https://slb.medv.ru/api/v2/', cert=(settings.CERTIFICATE, settings.CERTIFICATE_KEY),
                                    data=json.dumps(payload), headers=headers)
            if response.json()['error']['message'] == 'Method not found':
                response = 'Такого метода не существует!'
                print(response)
        except requests.ConnectionError as Error:
            response = 'Ошибка подключения к серверу: ' + str(Error)
            print(response)
        return HttpResponse(response)