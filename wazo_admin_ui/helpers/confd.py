# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask import g
from flask_login import current_user
from werkzeug.local import LocalProxy
from xivo_confd_client import Client as ConfdClient
from wazo_admin_ui.server import app


def get_confd_client():
    client = g.get('confd_client')
    if not client:
        client = g.confd_client = ConfdClient(**app.config['confd'])
        token = current_user.get_id()
        client.set_token(token)
    return client


confd = LocalProxy(get_confd_client)
