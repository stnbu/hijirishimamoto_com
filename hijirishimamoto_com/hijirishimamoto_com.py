# -*- coding: utf-8 -*-

import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
    flash, render_template_string, abort, send_from_directory, render_template, request
import smtplib
from email.mime.text import MIMEText


# create our little application :)
app = Flask(__name__)
app.secret_key = 'ngioewsnfewldjnfv jc gnkj cf nxjkhc fnj bfsz'


HTML = u"""<!DOCTYPE html>
<html>
<head>
<link rel="stylesheet" type="text/css" href="/static/style.css">
<link rel="shortcut icon" href="{{ url_for('static', filename='favicon.ico') }}">
</head>
<body>

<div class="menu">
{{ menu|safe }}
</div>

<div class="page-bg">
<div class="content">
{{ content|safe }}
</div>
</div>

</body>
</html>"""

PAGES = [
    'home',
    #'music',
    'biography',
    'lessons',
    'contact',
]


from wtforms import Form, BooleanField, StringField, PasswordField, validators, TextAreaField, TextField
class ContactForm(Form):
    name = StringField(u'Name', [validators.Length(max=200)])
    email = StringField(u'Email address', [validators.DataRequired(), validators.Email()])
    message = TextAreaField(u'Message', [validators.DataRequired(), validators.length(max=9000)])


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


# for certain broken browsers...
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

def send_mail(form):

    _from = 'noreply@unintuitive.org'
    to = 'hshimamoto@gmail.com'
    subject = 'Message from "{0} <{1}>"'.format(form.name.data, form.email.data)
    message = form.message.data

    message = MIMEText(form.message.data)
    message['Subject'] = subject
    message['From'] = _from
    message['To'] = to
    s = smtplib.SMTP('localhost')
    s.sendmail(_from, [to], message.as_string())
    s.quit()


@app.route('/<page_name>/', methods=['GET', 'POST'])
def pages(page_name):
    if page_name not in PAGES:
        abort(404)
    menu = get_menu(active=page_name)
    if request.method == 'POST':
        if page_name != 'contact':
            raise Exception('Not here!')
        form = ContactForm(request.form)
        send_mail(form)
        result = render_template_string(HTML, menu=menu, content='<div id="notification">Thank You. Your message has been sent.<div>')
        return result
    content = get_content(page_name)
    result = render_template_string(HTML, menu=menu, content=content)
    return result


if __name__ == '__main__':
    app.run('0.0.0.0', port=5005, debug=True)
