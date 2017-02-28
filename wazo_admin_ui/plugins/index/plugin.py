# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from wazo_admin_ui.helpers.plugin import create_blueprint

from .resource import Index

index = create_blueprint('index', __name__)


class Plugin(object):

    def load(self, dependencies):
        core = dependencies['flask']
        Index.register(index, route_base='/', route_prefix='')
        core.register_blueprint(index)
