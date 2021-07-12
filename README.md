ТЗ
---

Используя jsonrpc-2.0-API (ендпоинт: https://slb.medv.ru/api/v2/) создать Django-проект, при помощи которого можно вызвать метод api с использованием приложенной пары сертификат+ключ для авторизации ("двусторонний TLS").

Содержимое сертификата и ключа прописывается в settings.py в виде текстовых переменных (не путей к файлам).

Использовать только стандартную библиотеку python (помимо django).

Для примера вызывается jsonrpc-2.0 метод "auth.check".

Желательно чтобы было похоже на повторно используемый код, с обработкой ошибок, в виде отдельного метода для вызова любого jsonrpc-метода и т.п.

_________________

Запуск проекта
-------------
Это полностью готовый к запуску проект

1). Склонировать этот репозиторий к себе на диск.

2). Установить все зависимости (Python, Django) из файла "req.txt".

3). Перейти в каталог с проектом и написать команду "python manage.py runserver 8000".

4). В браузере перейти по ссылке "http://127.0.0.1:8000/api-auth/auth.check/", вместо "auth.check" можно писать любой метод, который нужно запустить.

