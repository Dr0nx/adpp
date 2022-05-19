""" Используем шаблонизатор Jinja2 """
from os.path import join
from jinja2 import Template


def render(template_name, folder='templates', **kwargs):
    """
    :param template_name: имя шаблона
    :param folder: папка в которой ищем шаблон
    :param kwargs: параметры для передачи в шаблон
    :return:
    """
    # Открываем шаблон по имени
    path_name = join(folder, template_name)
    with open(path_name, encoding='utf-8') as f:
        template = Template(f.read())
    # рендерим шаблон с параметрами
    return template.render(**kwargs)
