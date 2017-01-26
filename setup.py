#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from setuptools import find_packages
from setuptools import setup

setup(
    name='wazo-admin-ui',
    version='0.1',
    description='Wazo admin UI',
    author='Wazo Authors',
    author_email='dev.wazo@gmail.com',
    url='https://github.com/wazo-pbx/wazo-admin-ui',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    scripts=['bin/wazo-admin-ui'],
    entry_points={
        'wazo_admin_ui.plugins': [
            'admin = wazo_admin_ui.plugins.admin.plugin:Plugin',
            'authentication = wazo_admin_ui.plugins.authentication.plugin:Plugin',
            'index = wazo_admin_ui.plugins.index.plugin:Plugin',
        ]
    }
)
