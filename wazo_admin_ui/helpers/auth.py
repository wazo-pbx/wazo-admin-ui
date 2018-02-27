# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask import g
from flask_login import current_user
from werkzeug.local import LocalProxy
from xivo_auth_client import Client as AuthClient
from wazo_admin_ui.http_server import app


def _get_auth_client(config):
    client = g.get('auth_client')
    if not client:
        client = g.auth_client = AuthClient(**config)
    return client


def get_auth_client_from_session():
    config = app.config['auth']
    config['token'] = current_user.get_id()
    return _get_auth_client(config)


def get_auth_client(username, password):
    config = app.config['auth']
    config['username'] = username
    config['password'] = password
    return _get_auth_client(config)


auth = LocalProxy(get_auth_client_from_session)
