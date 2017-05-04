# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from hamcrest import assert_that, contains_string, equal_to, not_, calling, raises
from selenium.common.exceptions import TimeoutException

from .test_api.base import IntegrationTest
from .test_api.constants import REQUIRED_ERROR, USERNAME_PASSWORD_ERROR


class TestLogin(IntegrationTest):

    asset = 'base'

    def setUp(self):
        self.browser.logout()

    def test_empty_login(self):
        login = self.browser.login
        login.fill_name('username', '')
        login.fill_name('password', '')

        submit = login.driver.find_element_by_id('submit')
        assert_that(submit.get_attribute('class'), contains_string('disabled'))

        login.save(waiting=False)

        username = login.get_input_name('username')
        assert_that(username.get_error().text, equal_to(REQUIRED_ERROR))

        password = login.get_input_name('password')
        assert_that(password.get_error().text, equal_to(REQUIRED_ERROR))

    def test_invalid_login(self):
        login = self.browser.login
        login.fill_name('username', 'invalid')
        login.fill_name('password', 'invalid')

        submit = login.driver.find_element_by_id('submit')
        assert_that(submit.get_attribute('class'), not_(contains_string('disabled')))

        login.save(waiting=False)

        username = login.get_input_name('username')
        assert_that(username.get_error().text, equal_to(USERNAME_PASSWORD_ERROR))

        password = login.get_input_name('password')
        assert_that(password.get_error().text, equal_to(USERNAME_PASSWORD_ERROR))

    def test_cannot_access_without_login(self):
        assert_that(calling(self.browser.__getattr__).with_args('index'),
                    raises(TimeoutException))
