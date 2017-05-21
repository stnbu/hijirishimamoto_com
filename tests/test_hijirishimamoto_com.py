# -*- coding: utf-8 -*-
"""
    hijirishimamoto_com Tests
    ~~~~~~~~~~~~

    Tests the hijirishimamoto_com application.

    :copyright: (c) 2015 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""

import os
import tempfile
import pytest
from hijirishimamoto_com import hijirishimamoto_com


@pytest.fixture
def client(request):
    db_fd, hijirishimamoto_com.app.config['DATABASE'] = tempfile.mkstemp()
    hijirishimamoto_com.app.config['TESTING'] = True
    client = hijirishimamoto_com.app.test_client()
    with hijirishimamoto_com.app.app_context():
        hijirishimamoto_com.init_db()

    def teardown():
        os.close(db_fd)
        os.unlink(hijirishimamoto_com.app.config['DATABASE'])
    request.addfinalizer(teardown)

    return client


def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)


def test_empty_db(client):
    """Start with a blank database."""
    rv = client.get('/')
    assert b'No entries here so far' in rv.data


def test_login_logout(client):
    """Make sure login and logout works"""
    rv = login(client, hijirishimamoto_com.app.config['USERNAME'],
               hijirishimamoto_com.app.config['PASSWORD'])
    assert b'You were logged in' in rv.data
    rv = logout(client)
    assert b'You were logged out' in rv.data
    rv = login(client, hijirishimamoto_com.app.config['USERNAME'] + 'x',
               hijirishimamoto_com.app.config['PASSWORD'])
    assert b'Invalid username' in rv.data
    rv = login(client, hijirishimamoto_com.app.config['USERNAME'],
               hijirishimamoto_com.app.config['PASSWORD'] + 'x')
    assert b'Invalid password' in rv.data


def test_messages(client):
    """Test that messages work"""
    login(client, hijirishimamoto_com.app.config['USERNAME'],
          hijirishimamoto_com.app.config['PASSWORD'])
    rv = client.post('/add', data=dict(
        title='<Hello>',
        text='<strong>HTML</strong> allowed here'
    ), follow_redirects=True)
    assert b'No entries here so far' not in rv.data
    assert b'&lt;Hello&gt;' in rv.data
    assert b'<strong>HTML</strong> allowed here' in rv.data
