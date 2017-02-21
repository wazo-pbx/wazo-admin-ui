# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask import Blueprint

from flask_menu.classy import register_flaskview

from .resource import Dashboard

dashboard = Blueprint('dashboard', __name__, template_folder='templates',
                      static_folder='static', static_url_path='/%s' % __name__)


class Plugin(object):

    def load(self, dependencies):
        core = dependencies['flask']

        Dashboard.register(dashboard, route_base='/dashboard', route_prefix='')

        register_flaskview(dashboard, Dashboard)

        core.register_blueprint(dashboard)
