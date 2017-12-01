#!/usr/bin/env python3
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from setuptools import setup


setup(
    name='wazo_admin_ui_test_helpers',
    version='1.0.0',

    description='Wazo Admin UI test helpers',

    author='Wazo Authors',
    author_email='dev@wazo.community',
    packages=['wazo_admin_ui_test_helpers', 'wazo_admin_ui_test_helpers.pages'],
    package_dir={
        'wazo_admin_ui_test_helpers': 'suite/helpers',
        'wazo_admin_ui_test_helpers.pages': 'suite/helpers/pages',
    }
)
