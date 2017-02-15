#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from setuptools import find_packages
from setuptools import setup
from setuptools.command.build_py import build_py as _build_py


class build_py(_build_py):
    def run(self):
        self.run_command('compile_catalog')
        _build_py.run(self)


class BabelWrapper(object):

    def compile_catalog(self, *args, **kwargs):
        return self.babel.compile_catalog(*args, **kwargs)

    @property
    def babel(self):
        from babel.messages import frontend as babel
        return babel


babel_wrapper = BabelWrapper()
setup(
    name='wazo-admin-ui',
    version='0.1',
    description='Wazo admin UI',
    author='Wazo Authors',
    author_email='dev.wazo@gmail.com',
    url='https://github.com/wazo-pbx/wazo-admin-ui',
    packages=find_packages(),
    include_package_data=True,
    setup_requires=['babel'],
    install_requires=['babel'],
    zip_safe=False,
    scripts=['bin/wazo-admin-ui'],

    cmdclass={'build_py': build_py,
              'compile_catalog': babel_wrapper.compile_catalog},

    entry_points={
        'wazo_admin_ui.plugins': [
            'admin = wazo_admin_ui.plugins.admin.plugin:Plugin',
            'authentication = wazo_admin_ui.plugins.authentication.plugin:Plugin',
            'index = wazo_admin_ui.plugins.index.plugin:Plugin',
        ]
    }
)
