# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask import g
from flask_login import current_user
from werkzeug.local import LocalProxy
from wazo_plugind_client import Client as PlugindClient
from wazo_admin_ui.core.server import app


def get_plugind_client():
    client = g.get('plugind_client')
    if not client:
        client = g.plugind_client = PlugindClient(**app.config['plugind'])
        token = current_user.get_id()
        client.set_token(token)
    return client


plugind = LocalProxy(get_plugind_client)
