import os

template_dir = os.path.dirname(__file__)


def render_html(file_name, params=None):

    if params is None:
        params = {}

    with open(os.path.join(template_dir, file_name), 'r+') as f:
        file_str = f.read()

        for k, v in params.iteritems():
            file_str = file_str.replace('{ %s }' % k, v)

    return file_str


params = {
    'title': 'Baltazar',
    'name': 'Jan',
    'hour': '5',
    'am_pm': 'a.m.'
}

html_str = render_html('baltazar.html', params=params)
print html_str

