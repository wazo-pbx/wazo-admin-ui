# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import os

from xivo_test_helpers.asset_launching_test_case import AssetLaunchingTestCase

from .pages.browser import Browser
from .pages.page import Page


class AdminUIAssetLaunchingTestCase(AssetLaunchingTestCase):

    service = 'admin-ui'

    @classmethod
    def setUpClass(cls):
        super(AdminUIAssetLaunchingTestCase, cls).setUpClass()
        try:
            cls.browser = cls.setup_browser()
            cls.browser.start()
        except Exception:
            super(AdminUIAssetLaunchingTestCase, cls).tearDownClass()
            raise

    @classmethod
    def tearDownClass(cls):
        cls.browser.stop()
        super(AdminUIAssetLaunchingTestCase, cls).tearDownClass()

    @classmethod
    def setup_browser(cls):
        virtual = os.environ.get('VIRTUAL_DISPLAY', '1') == '1'
        username = os.environ.get('WEBI_USERNAME', 'root')
        password = os.environ.get('WEBI_PASSWORD', 'password')
        url = os.environ.get('ADMIN_UI_URL')
        if not url:
            port = cls.service_port(9296, 'admin-ui')
            url = 'https://localhost:{port}'.format(port=port)
        Page.CONFIG['base_url'] = url
        return Browser(username, password, virtual)
