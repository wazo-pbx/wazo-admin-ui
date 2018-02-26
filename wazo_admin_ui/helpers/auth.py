# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask import g
from flask_login import current_user
from werkzeug.local import LocalProxy
from xivo_auth_client import Client as AuthClient
from wazo_admin_ui.http_server import app


def get_auth_client(username=None, password=None):
    client = g.get('auth_client')
    if not client:
        config = app.config['auth']
        if username and password:
            config['username'] = username
            config['password'] = password
        else:
            token = current_user.get_id()
            config['token'] = token
        client = g.auth_client = AuthClient(**config)
    return client


auth = LocalProxy(get_auth_client)
