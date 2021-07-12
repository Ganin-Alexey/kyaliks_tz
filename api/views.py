import os
from django.conf import settings
from django.views import View
from django.http import JsonResponse
import json
import tempfile
import http.client


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
            connection = http.client.HTTPSConnection('slb.medv.ru', key_file=key.name, cert_file=cert.name)
            connection.request('POST', '/api/v2/', body=json.dumps(payload), headers=headers)
            response = connection.getresponse().read()
            response_json = json.loads(response.decode('utf8').replace("'", '"'))

            if 'error' in response_json and response_json['error']['message'] == 'Method not found':
                response_json = 'Not found method - ' + str(response_json)
                return JsonResponse({'answer': response_json})
        except:
            response_json = 'Server connection error'

        # Закрываем и удаляем все временные файлы
        key.close()
        cert.close()
        os.unlink(cert.name)
        os.unlink(key.name)
        return JsonResponse({'answer': response_json})