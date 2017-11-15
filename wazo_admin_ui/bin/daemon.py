# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import sys

from xivo import xivo_logging
from xivo.daemonize import pidfile_context
from xivo.user_rights import change_user
from wazo_admin_ui.config import load as load_config
from wazo_admin_ui.controller import Controller


def main():
    config = load_config(sys.argv[1:])

    if config.get('user'):
        change_user(config['user'])

    xivo_logging.setup_logging(config['log_filename'],
                               config['foreground'],
                               config['debug'],
                               config['log_level'])

    controller = Controller(config)

    with pidfile_context(config['pid_filename'], config['foreground']):
        controller.run()
