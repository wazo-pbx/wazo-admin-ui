# Copyright 2017-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_babel import lazy_gettext as l_
from wazo_admin_ui.helpers.destination import register_destination_form

from .form import (
    ApplicationDestination,
    CustomDestination,
    HangupDestination,
    NoneDestination
)


class Plugin():

    def load(self, dependencies):
        register_destination_form('application', l_('Application'), ApplicationDestination)
        register_destination_form('hangup', l_('Hangup'), HangupDestination)
        register_destination_form('custom', l_('Custom'), CustomDestination)
        register_destination_form('none', l_('None'), NoneDestination, position=0)
