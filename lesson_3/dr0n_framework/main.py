import quopri
from dr0n_framework.requests import GetRequests, PostRequests


class PageNotFound404:
    def __call__(self, request):
        return '404', '404 page not found'


class Framework:

    # Класс Framework - основа WSGI-фреймворка

    def __init__(self, routes_obj):
        self.routes_lst = routes_obj

    def __call__(self, environ, start_response):
        # Получаем адрес, по которому пользователь выполнил переход
        path = environ['PATH_INFO']

        # Добавляем закрывающий слеш
        if not path.endswith('/'):
            path = f'{path}/'

        request = dict()
        # Получаем все данные запроса
        method = environ['REQUEST_METHOD']
        request['method'] = method

        if method == 'POST':
            data = PostRequests().get_request_params(environ)
            request['data'] = data
            print(f'Пришёл POST-запрос: {Framework.decode_value(data)}')
        if method == 'GET':
            request_params = GetRequests().get_request_params(environ)
            request['request_params'] = request_params
            print(f'Пришли GET-параметры: {request_params}')

        # Находим нужный контроллер
        if path in self.routes_lst:
            view = self.routes_lst[path]
        else:
            view = PageNotFound404()

        # Запускаем контроллер
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

    @staticmethod
    def decode_value(data):
        # Убираем "кракозябры"
        new_data = dict()
        for key, value in data.items():
            # Меняем "%" и "+" на "=" и " "
            value_replace = bytes(value.replace('%', '=').replace('+', ' '), 'UTF-8')
            # Переводим из байтов в строку
            new_data[key] = quopri.decodestring(value_replace).decode('UTF-8')
        return new_data
