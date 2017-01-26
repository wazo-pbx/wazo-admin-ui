# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import logging

from flask import render_template

from flask_classful import FlaskView
from flask_menu.classy import classy_menu_item
from flask_security.decorators import login_required

logger = logging.getLogger(__name__)


class Admin(FlaskView):
    decorators = [login_required]

    @classy_menu_item('.dashboard', 'Dashboard', order=0, icon="dashboard")
    def get(self):
        return render_template('admin.html')
