# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from xivo_test_helpers.asset_launching_test_case import AssetLaunchingTestCase
from xivo_test_helpers.admin_ui.asset_launching_test_case import AdminUIAssetLaunchingTestCase

from .constants import ASSET_ROOT

from .pages.index import IndexPage


class SSLIntegrationTest(AssetLaunchingTestCase):

    assets_root = ASSET_ROOT
    service = 'admin-ui'


class IntegrationTest(AdminUIAssetLaunchingTestCase):

    assets_root = ASSET_ROOT

    @classmethod
    def setup_browser(cls):
        browser = AdminUIAssetLaunchingTestCase.setup_browser()
        browser.pages['index'] = IndexPage
        return browser
