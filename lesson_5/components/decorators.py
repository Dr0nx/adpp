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
