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
<meta name="keywords" content="saxophone, sax, piano, clarinet, music lesson, milpitas, san jose, fremont, south bay area, bay area, silicon valley, online, experienced, japanese, female, bilingual" />
<title>Lessons</title>
<link rel="stylesheet" type="text/css" href="/static/style.css">
<link rel="shortcut icon" href="{{ url_for('static', filename='favicon.ico') }}">
{{ head|safe }}
</head>
<body>

<div class="menu">
{{ menu|safe }}
</div>

<div class="content">
{{ content|safe }}
</div>

</body>
</html>"""

PAGES = [
    'home',
    'biography',
    'philosophy',
    'music',
    'lessons',
    'access',
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

    name = form.name.data.encode('utf-8')
    message = form.message.data.encode('utf-8')
    email = form.email.data.encode('utf-8')

    _from = 'noreply@unintuitive.org'
    to = 'hshimamoto@gmail.com'
    subject = 'Message from "{0} <{1}>"'.format(name, email)

    message = MIMEText(message)
    message['Subject'] = subject
    message['From'] = _from
    message['To'] = to
    s = smtplib.SMTP('localhost')
    s.sendmail(_from, [to], message.as_string())
    s.quit()

def get_head(page_name):
    'hack. i dont care.'
    head = ''
    if page_name not in ['home', 'music']:
        head = """
            <style>
                .content {
                    margin: 0 auto;
                }
            </style>
        """
    if page_name in ['home', 'music']:

        if page_name == 'home':
            padding = '100px'
        elif page_name == 'music':
            padding = 'top'

        head = """
            <style>
                body {{
                    background-image: url(/static/{page_name}.jpg);
                    background-color: rgb(0, 0, 0);
                    background-position: center {background_img_top_padding};
                }}
                .content {{
                    display: inline-block;
                    width: auto;
                }}
            </style>
        """.format(
            page_name=page_name,
            background_img_top_padding=padding,
        )

    return head


@app.route('/<page_name>/', methods=['GET', 'POST'])
def pages(page_name):
    if page_name not in PAGES:
        abort(404)
    head = get_head(page_name)
    menu = get_menu(active=page_name)
    if request.method == 'POST':
        if page_name != 'contact':
            raise Exception('Not here!')
        form = ContactForm(request.form)
        send_mail(form)
        result = render_template_string(HTML, menu=menu, content='<div id="notification">Thank You. Your message has been sent.<div>')
        return result
    content = get_content(page_name)
    result = render_template_string(HTML,
                                    head=head,
                                    menu=menu,
                                    content=content)
    return result


if __name__ == '__main__':
    app.run('0.0.0.0', port=5005, debug=True)
