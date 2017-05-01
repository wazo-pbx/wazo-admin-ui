# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from wazo_admin_ui.helpers.destination import register_destination_form

from .form import NoneDestination


class Plugin(object):

    def load(self, dependencies):
        register_destination_form('none', 'None', NoneDestination)
