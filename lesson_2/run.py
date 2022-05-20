from wsgiref.simple_server import make_server
from dr0n_framework.main import Framework
from urls import routes

app = Framework(routes)

with make_server('', 8000, app) as httpd:
    print('Запускаю сервер на порту 8000...')
    httpd.serve_forever()
