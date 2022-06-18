from time import time


# Декоратор для реализации маршрутизации
class AppRoute:
    def __init__(self, routes, url):
        """
        Сохраняем значение переданного параметра
        :param routes:
        :param url:
        :return:
        """
        self.routes = routes
        self.url = url

    def __call__(self, cls):
        """
        Сам декоратор
        :param cls:
        :return:
        """
        self.routes[self.url] = cls()


def debug(func):
    def wrapped(*args, **kwargs):
        print(f'Имя функции {func.__name__}, время -', end=' ')
        start = time()
        result = func(*args, **kwargs)
        stop = time()
        print(stop - start)
        return result

    return wrapped
