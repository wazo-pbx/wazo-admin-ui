# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask import g
from flask_login import current_user
from werkzeug.local import LocalProxy
from wazo_call_logd_client import Client as CallLogdClient
from wazo_admin_ui.http_server import app


def get_call_logd_client():
    client = g.get('call_logd_client')
    if not client:
        client = g.call_logd_client = CallLogdClient(**app.config['call_logd'])
        token = current_user.get_id()
        client.set_token(token)
    return client


call_logd = LocalProxy(get_call_logd_client)
