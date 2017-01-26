# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask import Blueprint

from .resource import Index

index = Blueprint('index', __name__, template_folder='templates',
                  static_folder='static', static_url_path='/%s' % __name__)


class Plugin(object):

    def load(self, dependencies):
        core = dependencies['flask']
        Index.register(index, route_base='/', route_prefix='')
        core.register_blueprint(index)
