import quopri
from os import path

from components.content_types import CONTENT_TYPES_MAP
from dr0n_framework.requests import GetRequests, PostRequests


class PageNotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


class Framework:
    # Класс Framework - основа WSGI-фреймворка

    def __init__(self, settings, routes_obj):
        self.routes_lst = routes_obj
        self.settings = settings

    def __call__(self, environ, start_response):
        # Получаем адрес, по которому пользователь выполнил переход
        path_info = environ.get('PATH_INFO')

        # Добавляем закрывающий слэш
        if not path_info.endswith('/'):
            path_info = f'{path_info}/'

        request = dict()
        # Получаем все данные запроса
        method = environ['REQUEST_METHOD']
        request['method'] = method

        if method == 'POST':
            data = PostRequests().get_request_params(environ)
            request['data'] = data
        if method == 'GET':
            request_params = GetRequests().get_request_params(environ)
            request['request_params'] = request_params

        # Находим нужный контроллер
        if path_info in self.routes_lst:
            view = self.routes_lst[path_info]
            content_type = self.get_content_type(path_info)
            code, body = view(request)
            body = body.encode('utf-8')
        elif path_info.startswith(self.settings.STATIC_URL):
            file_path = path_info[len(self.settings.STATIC_URL):len(path_info) - 1]
            content_type = self.get_content_type(file_path)
            code, body = self.get_static(self.settings.STATIC_FILES_DIR, file_path)
        else:
            view = PageNotFound404()
            content_type = self.get_content_type(path_info)
            code, body = view(request)
            body = body.encode('utf-8')
        start_response(code, [('Content-Type', content_type)])

        return [body]

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

    @staticmethod
    def decode_value(data):
        new_data = dict()
        for key, value in data.items():
            val = bytes(value.replace('%', '=').replace("+", " "), 'UTF-8')
            val_decode_str = quopri.decodestring(val).decode('UTF-8')
            new_data[key] = val_decode_str
        return new_data
