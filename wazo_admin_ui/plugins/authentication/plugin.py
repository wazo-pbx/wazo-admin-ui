# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask import Blueprint

from .resource import Login, Logout

login = Blueprint('login',
                  __name__,
                  template_folder='templates',
                  static_folder='static',
                  static_url_path='/%s' % __name__)

logout = Blueprint('logout',
                   __name__,
                   template_folder='templates',
                   static_folder='static',
                   static_url_path='/%s' % __name__)


class Plugin(object):

    def load(self, dependencies):
        core = dependencies['flask']

        Login.register(login, route_base='/login', route_prefix='')
        core.register_blueprint(login)

        Logout.register(logout, route_base='/logout', route_prefix='')
        core.register_blueprint(logout)
