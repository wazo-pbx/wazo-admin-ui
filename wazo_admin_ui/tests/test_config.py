# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import unittest

from hamcrest import assert_that, contains_inanyorder, empty

from ..config import _extract_enabled_plugins


class TestConfig(unittest.TestCase):

    def test_extract_enabled_plugins(self):
        config = {'plugin1': False,
                  'plugin2': True,
                  'plugin3': False,
                  'plugin4': True}

        enabled_plugins = _extract_enabled_plugins(config)

        assert_that(enabled_plugins, contains_inanyorder('plugin2', 'plugin4'))

    def test_extract_enabled_plugins_when_all_disabled(self):
        config = {'plugin1': False,
                  'plugin2': False}

        enabled_plugins = _extract_enabled_plugins(config)

        assert_that(enabled_plugins, empty())
