# -*- coding: utf-8 -*-

import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
    flash, render_template_string, abort


# create our little application :)
app = Flask(__name__)



HTML = u"""<!DOCTYPE html>
<html>
<head>
<link rel="stylesheet" type="text/css" href="/static/style.css">
</head>
<body>
{{ menu|safe }}

<div class="content">
{{ content|safe }}
</div>

</body>
</html>"""

PAGES = [
    'home',
    'music',
    'biography',
    'lessons',
    'contact',
]

def get_content(page_name):
    my_dir = os.path.dirname(os.path.realpath(__file__))
    my_file = os.path.join(my_dir, 'pages', '{0}.html'.format(page_name))
    with open(my_file, 'r') as f:
        return f.read().decode('utf-8')


def get_menu(active):
    menu = ['<ul>']
    for page in PAGES:
        title = page.capitalize()
        if page == active:
            style = 'class="active"'
        else:
            style = ''
        menu.append('<li><a {0} href="/{1}/">{2}</a></li>'.format(style, page, title))
    menu.append('</ul>')
    return '\n'.join(menu)

@app.route('/')
def root():
    return redirect('/home/')

@app.route('/<page_name>/')
def pages(page_name):
    if page_name not in PAGES:
        abort(404)
    menu = get_menu(active=page_name)
    content = get_content(page_name)
    result = render_template_string(HTML, menu=menu, content=content)
    return result


if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
