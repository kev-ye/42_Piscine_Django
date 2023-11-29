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

def render(argv: list):
    if not handle_args(argv):
        print('Usage: python render.py <file.template>', file=sys.stderr)
        return

    if template_data := load_template(argv[1]):
        res = re.findall(r'{([^{]*?)}', template_data)
        print('->', res)


if __name__ == '__main__':
    print(settings_data)
    print('len:', len(settings_data))

    render(sys.argv)
