import quopri
from os import path
from components.content_types import CONTENT_TYPES_MAP


class PageNotFound404:
    def __call__(self, request):
        return '404', '404 page not found'


class Framework:

    # Класс Framework - основа WSGI-фреймворка

    def __init__(self, settings, routes_obj):
        self.routes_lst = routes_obj
        self.settings = settings

    def __call__(self, environ, start_response):
        # Получаем адрес, по которому пользователь выполнил переход
        path_info = environ['PATH_INFO']

        # Добавляем закрывающий слеш
        if not path_info.endswith('/'):
            path_info = f'{path_info}/'

        request = dict()
        # Получаем все данные запроса
        method = environ['REQUEST_METHOD']
        request['method'] = method

        # Находим нужный контроллер
        if path_info in self.routes_lst:
            view = self.routes_lst[path_info]
            content_type = self.get_content_type(path_info)
            code, body = view(request)
            body = body.encode('utf-8')
        elif path_info.startswith(self.settings.STATIC_URL):
            # /static/images/logo.jpg/ -> images/logo.jpg
            file_path = path_info[len(self.settings.STATIC_URL):len(path_info) - 1]
            content_type = self.get_content_type(file_path)
            code, body = self.get_static(self.settings.STATIC_FILES_DIR,
                                         file_path)
        else:
            view = PageNotFound404()
            content_type = self.get_content_type(path_info)
            code, body = view(request)
            body = body.encode('utf-8')
        start_response(code, [('Content-Type', content_type)])

        return [body]

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

    @staticmethod
    def get_content_type(file_path, content_types_map=CONTENT_TYPES_MAP):
        file_name = path.basename(file_path).lower()  # styles.css
        extension = path.splitext(file_name)[1]  # .css
        return content_types_map.get(extension, "text/html")

    @staticmethod
    def get_static(static_dir, file_path):
        path_to_file = path.join(static_dir, file_path)
        with open(path_to_file, 'rb') as f:
            file_content = f.read()
        status_code = '200 OK'
        return status_code, file_content
