# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask import url_for, redirect
from flask_classful import FlaskView


class Index(FlaskView):

    def get(self):
        return redirect(url_for('login.Login:get'))
