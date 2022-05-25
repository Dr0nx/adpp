from jinja2 import FileSystemLoader
from jinja2.environment import Environment


def render(template_name, folder='templates', static_url='/static/', **kwargs):
    environ = Environment()
    environ.loader = FileSystemLoader(folder)
    environ.globals['static'] = static_url
    template = environ.get_template(template_name)
    return template.render(**kwargs)
