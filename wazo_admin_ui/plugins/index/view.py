# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask import url_for, redirect, render_template
from flask_classful import FlaskView
from flask_login import current_user


class Index(FlaskView):

    def get(self):
        if not current_user.is_authenticated:
            return redirect(url_for('login.Login:get'))

        return render_template('index.html')
