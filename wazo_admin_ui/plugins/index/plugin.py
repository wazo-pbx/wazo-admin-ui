# Copyright 2017-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from wazo_admin_ui.helpers.plugin import create_blueprint

from .view import Index

index = create_blueprint('index', __name__)


class Plugin():

    def load(self, dependencies):
        core = dependencies['flask']
        Index.register(index, route_base='/', route_prefix='')
        core.register_blueprint(index)
