# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask import g
from flask_login import current_user
from werkzeug.local import LocalProxy
from xivo_call_logs_client import Client as CallLogdClient
from wazo_admin_ui.core.server import app


def get_calllogd_client():
    client = g.get('calllogd_client')
    if not client:
        client = g.calllogd_client = CallLogdClient(**app.config['call_logd'])
        token = current_user.get_id()
        client.set_token(token)
    return client


calllogd = LocalProxy(get_calllogd_client)
