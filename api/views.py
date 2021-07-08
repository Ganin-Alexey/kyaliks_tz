import os
from django.conf import settings
from django.views import View
from django.http import HttpResponse
import requests
import json
import tempfile


class AuthAPI(View):
    def get(self, request, method_name='auth.check'):
        headers = {'content-type': 'application/json'}
        payload = {
            "method": method_name,
            "params": {},
            "jsonrpc": "2.0",
            "id": 0,
        }
        # Создание временных файлов и запись в них сертификатов
        cert = tempfile.TemporaryFile(delete=False, dir=settings.BASE_DIR, mode="w+", encoding='utf-8', suffix='.crt')
        cert.write(settings.CERTIFICATE)
        key = tempfile.TemporaryFile(delete=False, dir=settings.BASE_DIR, mode="w+", encoding='utf-8', suffix='.key')
        key.write(settings.CERTIFICATE_KEY)
        cert.read()
        key.read()
        # Подключение к endpoint и обработка ошибок
        try:
            response = requests.post('https://slb.medv.ru/api/v2/', cert=(cert.name, key.name),
                                data=json.dumps(payload), headers=headers)
            if 'error' in response and response.json()['error']['message'] == 'Method not found':
                response = 'Такого метода не существует!'
                # Для вывода ошибки в консоль
                print(response)
        except requests.ConnectionError as Error:
            response = 'Ошибка подключения к серверу: ' + str(Error)
            # Для вывода ошибки в консоль
            print(response)
        # Закрываем и удаляем все временные файлы
        key.close()
        cert.close()
        os.unlink(cert.name)
        os.unlink(key.name)
        return HttpResponse(response)