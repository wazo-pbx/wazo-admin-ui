# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from hamcrest import assert_that
from hamcrest import contains_string
from xivo_test_helpers import until

from .test_api.base import IntegrationTest


class TestHTTPSMissingCertificate(IntegrationTest):
    asset = 'no_ssl_certificate'

    def test_given_no_ssl_certificate_when_admin_ui_starts_then_admin_ui_stops(self):
        def _is_stopped():
            status = self.service_status()
            return not status['State']['Running']

        until.true(_is_stopped, tries=10, message='wazo-admin-ui did not stop while missing SSL certificate')

        log = self.service_logs()
        assert_that(log, contains_string("No such file or directory: '/usr/share/xivo-certs/server.crt'"))


class TestHTTPSMissingPrivateKey(IntegrationTest):
    asset = 'no_ssl_private_key'

    def test_given_no_ssl_private_key_when_admin_ui_starts_then_admin_ui_stops(self):
        def _is_stopped():
            status = self.service_status()
            return not status['State']['Running']

        until.true(_is_stopped, tries=10, message='wazo-admin-ui did not stop while missing SSL private key')

        log = self.service_logs()
        assert_that(log, contains_string("No such file or directory: '/usr/share/xivo-certs/server.key'"))
