#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from setuptools import find_packages
from setuptools import setup
from setuptools.command.install_lib import install_lib as _install_lib
from distutils.command.build import build as _build


class build(_build):
    sub_commands = [('compile_catalog', None)] + _build.sub_commands


class install_lib(_install_lib):
    def run(self):
        self.run_command('compile_catalog')
        _install_lib.run(self)


class BabelWrapper(object):

    @property
    def compile_catalog(self):
        return self.babel.compile_catalog

    @property
    def extract_messages(self):
        return self.babel.extract_messages

    @property
    def init_catalog(self):
        return self.babel.init_catalog

    @property
    def update_catalog(self):
        return self.babel.update_catalog

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

    cmdclass={'build': build,
              'install_lib': install_lib,
              'compile_catalog': babel_wrapper.compile_catalog,
              'extract_messages': babel_wrapper.extract_messages,
              'init_catalog': babel_wrapper.init_catalog,
              'update_catalog': babel_wrapper.update_catalog},

    entry_points={
        'wazo_admin_ui.plugins': [
            'admin = wazo_admin_ui.plugins.admin.plugin:Plugin',
            'authentication = wazo_admin_ui.plugins.authentication.plugin:Plugin',
            'index = wazo_admin_ui.plugins.index.plugin:Plugin',
        ]
    }
)
