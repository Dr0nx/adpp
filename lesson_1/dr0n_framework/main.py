class PageNotFound:
    def __call__(self, *args, **kwargs):
        return '404 ?', '404 page not found'


class Framework:
    """ Этот класс Framework - основа WSGI-фреймворка """

    def __init__(self, routes_obj):
        self.routes_lst = routes_obj

    def __call__(self, environ, start_response):
        # Получаем адрес, по которому пользователь выполнил переход
        path = environ.get('PATH_INFO')

        # Добавляем закрывающий слэш, без него могут быть проблемы
        if not path.endswith('/'):
            path = f'{path}'

        # Здесь указываем необходимый контроллер
        if path in self.routes_lst:
            view = self.routes_lst[path]
        else:
            view = PageNotFound()

        # Запускем контроллер
        code, body = view()
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]
