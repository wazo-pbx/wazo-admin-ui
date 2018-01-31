# Copyright 2017-2018 The Wazo Authors  (see the AUTHORS file)
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
        username = 'xivo-auth-mock-doesnt-care-about-username'
        password = 'xivo-auth-mock-doesnt-care-about-password'
        port = cls.service_port(9296, 'admin-ui')
        Page.CONFIG['base_url'] = 'https://localhost:{port}'.format(port=port)
        return Browser(username, password, virtual)
