from wsgiref.simple_server import make_server

from dr0n_framework.main import Framework
from views import routes
from components import settings

# Создаем объект WSGI-приложения
application = Framework(settings, routes)

with make_server('', 8000, application) as httpd:
    print("Запускаю на порту 8000...")
    httpd.serve_forever()
