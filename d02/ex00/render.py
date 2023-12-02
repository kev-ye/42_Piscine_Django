import sys
import os
import re


config_root_path = os.path.dirname(os.path.abspath(__file__))
config_setting_file = config_root_path + '/settings.py'

try:
    with open(config_setting_file, 'r') as config_f:
        exec(config_f.read())
except (FileNotFoundError, PermissionError):
    exit('settings.py not found or permission denied')

settings_data = {
    k: v for k, v in globals().items()
    if (not k.startswith('__')
        and not k.startswith('config_')
        and k not in ('os', 'sys', 're'))
}

def load_template(file_path: str):
    template_data = None
    try:
        with open(file_path, 'r') as template_f:
            template_data = template_f.read()
    except (FileNotFoundError, PermissionError):
        print('File not found or permission denied', file=sys.stderr)

    return template_data

def handle_args(argv: list):
    if len(argv) != 2 or not argv[1].endswith('.template'):
        return False
    return True

def render_html(file_name: str, template_data: str, settings_data: dict, ls_data_to_replace: list):
    for data in ls_data_to_replace:
        template_data = template_data.replace('{' + data + '}', str(settings_data[data]))

    try:
        with open(file_name, 'w') as html_f:
            html_f.write(template_data)
    except PermissionError:
        print('Cannot write to file', file=sys.stderr)


def render(argv: list, settings_data: dict):
    if not handle_args(argv):
        print('Usage: python render.py <file.template>', file=sys.stderr)
        return

    if template_data := load_template(argv[1]):
        ls_data_to_replace = re.findall(r'{([^{]*?)}', template_data)

        if (ls_data_to_replace := set(ls_data_to_replace)) - set(settings_data.keys()):
            print('All keys in template must be in settings.py', file=sys.stderr)
            return
        
        html_name = argv[1][:-9] + '.html'
        render_html(html_name, template_data, settings_data, ls_data_to_replace)


if __name__ == '__main__':
    render(sys.argv, settings_data)
