# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import os

from xivo_test_helpers.asset_launching_test_case import AssetLaunchingTestCase

from .constants import ASSET_ROOT
from .pages.browser import Browser
from .pages.page import Page


class IntegrationTest(AssetLaunchingTestCase):

    assets_root = ASSET_ROOT
    service = 'admin-ui'

    @classmethod
    def setUpClass(cls):
        super(IntegrationTest, cls).setUpClass()
        cls.browser = cls.setup_browser()
        cls.browser.start()

    @classmethod
    def tearDownClass(cls):
        cls.browser.stop()
        super(IntegrationTest, cls).tearDownClass()

    @classmethod
    def setup_browser(cls):
        virtual = os.environ.get('VIRTUAL_DISPLAY', '1') == '1'
        username = os.environ.get('WEBI_USERNAME', 'root')
        password = os.environ.get('WEBI_PASSWORD', 'proformatique')
        url = os.environ.get('ADMIN_UI_URL')
        if not url:
            port = cls.service_port(9296, 'admin-ui')
            url = 'https://localhost:{port}'.format(port=port)
        Page.CONFIG['base_url'] = url
        return Browser(username, password, virtual)
