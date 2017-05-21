# -*- coding: utf-8 -*-

import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
    flash, render_template_string


# create our little application :)
app = Flask(__name__)


from flask import render_template_string

HTML = u"""<!DOCTYPE html>
<html>
<head>
<style>
ul {
    list-style-type: none;
    margin: 0;
    padding: 0;
    overflow: hidden;
    background-color: #333;
}

li {
    float: left;
}

li a {
    display: block;
    color: white;
    text-align: center;
    padding: 14px 16px;
    text-decoration: none;
}

li a:hover:not(.active) {
    background-color: #111;
}

.active {
    background-color: #4CAF50;
}
</style>
</head>
<body>
{{ menu|safe }}

<div>
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
    assert page_name in PAGES, '{0} was not in allowed pages.'.format(page_name)
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
        menu.append('<li><a {0} href="/{1}">{2}</a></li>'.format(style, page, title))
    menu.append('</ul>')
    return '\n'.join(menu)

@app.route('/<page_name>')
def pages(page_name):
    menu = get_menu(active=page_name)
    content = get_content(page_name)
    result = render_template_string(HTML, menu=menu, content=content)
    return result
