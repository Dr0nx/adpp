from jinja2 import FileSystemLoader
from jinja2.environment import Environment


def render(template_name, folder='templates', **kwargs):
    """
    :param template_name: имя шаблона
    :param kwargs: параметры для передачи в шаблон
    :return:
    """
    environ = Environment()
    environ.loader = FileSystemLoader(folder)
    template = environ.get_template(template_name)
    return template.render(**kwargs)
