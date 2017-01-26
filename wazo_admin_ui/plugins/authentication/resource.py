# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import logging

from flask import url_for, render_template, redirect
from flask_classful import FlaskView
from flask_login import login_user, logout_user

from .form import LoginForm

logger = logging.getLogger(__name__)


class Login(FlaskView):

    def get(self):
        return self._login()

    def post(self):
        return self._login()

    def _login(self):
        form = LoginForm()
        if form.validate_on_submit():
            login_user(form.user)
            return redirect(url_for('admin.Admin:get'))

        return render_template('login.html',
                               login_user_form=form)


class Logout(FlaskView):

    def get(self):
        logout_user()
        return redirect(url_for('index.Index:get'))
