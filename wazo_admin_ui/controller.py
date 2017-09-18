# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import logging

from xivo import plugin_helpers
from .http_server import Server

logger = logging.getLogger(__name__)


class Controller(object):

    def __init__(self, config):
        self.server = Server(config)
        plugin_helpers.load(
            namespace='wazo_admin_ui.plugins',
            names=config['enabled_plugins'],
            dependencies={
                'config': config,
                'flask': self.server.get_app(),
            }
        )

    def run(self):
        logger.info('wazo-admin-ui starting...')
        try:
            self.server.run()
        finally:
            logger.info('wazo-admin-ui stopping...')
