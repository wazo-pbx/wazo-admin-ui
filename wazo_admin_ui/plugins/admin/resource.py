# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import logging

from flask import render_template

from flask_classful import FlaskView
from flask_login import login_required
from flask_menu.classy import classy_menu_item

logger = logging.getLogger(__name__)


class Admin(FlaskView):

    @classy_menu_item('.dashboard', 'Dashboard', order=0, icon="dashboard")
    @login_required
    def get(self):
        return render_template('admin.html')
