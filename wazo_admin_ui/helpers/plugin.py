# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask import Blueprint


def create_blueprint(name, import_name):
    return Blueprint(name, import_name, template_folder='templates',
                     static_folder='static', static_url_path='/%s' % import_name)
