# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import unittest

from flask import Flask
from hamcrest import assert_that, contains, empty, is_, equal_to
from mock import Mock
from wtforms import StringField

from ..classful import BaseView, _is_positive_integer, extract_select2_params, build_select2_response
from ..error import ErrorExtractor, ErrorTranslator
from ..form import BaseForm

URL_TO_NAME_RESOURCES = {'resources_url': 'resource'}

GENERIC_PATTERN_ERRORS = {'invalid-data': r'^Input Error'}
GENERIC_MESSAGE_ERRORS = {'invalid-data': 'Input Error'}

SPECIFIC_PATTERN_ERRORS = {'invalid-length': r'Longer than maximum length'}
SPECIFIC_MESSAGE_ERRORS = {'invalid-length': 'Longer than maximum length'}

app = Flask('test_wazo_admin_ui')


class TestBaseView(unittest.TestCase):

    def setUp(self):
        self.view = BaseView()
        ErrorExtractor.generic_patterns = GENERIC_PATTERN_ERRORS
        ErrorExtractor.specific_patterns = SPECIFIC_PATTERN_ERRORS
        ErrorExtractor.url_to_name_resources = URL_TO_NAME_RESOURCES
        ErrorTranslator.generic_messages = GENERIC_MESSAGE_ERRORS
        ErrorTranslator.specific_messages = SPECIFIC_MESSAGE_ERRORS
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False

        class MyForm(BaseForm):
            attribute1 = StringField()

        with app.test_request_context(method='POST', data={'attribute1': ''}):
            self.form = MyForm()

    def test_fill_form_error_with_confd_input_error(self):
        confd_error = ["Input Error - attribute1: 'Longer than maximum length'"]
        path_url = '/1.1/resources_url/42'
        form = self.view._fill_form_error(self.form, self._build_error(confd_error, path_url))

        assert_that(form.attribute1.errors, contains('Longer than maximum length'))

    def test_fill_form_error_with_confd_input_error_and_not_register_msg(self):
        confd_error = ["Input Error - attribute1: 'Unregistered message'"]
        path_url = '/1.1/resources_url/42'
        form = self.view._fill_form_error(self.form, self._build_error(confd_error, path_url))

        assert_that(form.attribute1.errors, empty())

    def test_fill_form_error_with_confd_input_error_and_invalid_attribute(self):
        confd_error = ["Input Error - invalid_attr: 'Longer than maximum length'"]
        path_url = '/1.1/resources_url/42'
        form = self.view._fill_form_error(self.form, self._build_error(confd_error, path_url))

        assert_that(form.attribute1.errors, empty())

    def test_fill_form_error_with_confd_input_error_and_invalid_format(self):
        confd_error = ["Input Error - field 'users': User was not found ('uuid': 'patate')"]
        path_url = '/1.1/resources_url/42'
        form = self.view._fill_form_error(self.form, self._build_error(confd_error, path_url))

        assert_that(form.attribute1.errors, empty())

    def test_fill_form_error_with_confd_not_input_error(self):
        confd_error = ["Some Error - "]
        path_url = '/1.1/resources_url/42'
        form = self.view._fill_form_error(self.form, self._build_error(confd_error, path_url))

        assert_that(form.attribute1.errors, empty())

    def _build_error(self, error, path_url):
        return Mock(response=Mock(json=Mock(return_value=error)),
                    request=Mock(path_url=path_url))


class TestSelect2Helpers(unittest.TestCase):

    def test_is_positive_integer(self):
        response = _is_positive_integer(1)
        assert_that(response, is_(True))

    def test_is_positive_integer_when_string_integer(self):
        response = _is_positive_integer('1')
        assert_that(response, is_(True))

    def test_is_positive_integer_when_none(self):
        response = _is_positive_integer(None)
        assert_that(response, is_(False))

    def test_is_positive_integer_when_negative(self):
        response = _is_positive_integer(-1)
        assert_that(response, is_(False))

    def test_is_positive_integer_when_string(self):
        response = _is_positive_integer('abcd')
        assert_that(response, is_(False))

    def test_extract_select2_params(self):
        args = {'term': 'a', 'page': 1}
        result = extract_select2_params(args, limit=10)
        assert_that(result, equal_to({'search': 'a',
                                      'offset': 0,
                                      'limit': 10}))

    def test_extract_select2_params_when_no_args(self):
        args = {}
        result = extract_select2_params(args, limit=10)
        assert_that(result, equal_to({'search': None,
                                      'offset': 0,
                                      'limit': 10}))

    def test_extract_select2_params_when_page_is_not_positive_integer(self):
        args = {'page': 'abcd'}
        result = extract_select2_params(args, limit=10)
        assert_that(result, equal_to({'search': None,
                                      'offset': 0,
                                      'limit': 10}))

    def test_extract_select2_params_when_page_is_more_than_one(self):
        args = {'page': 3}
        result = extract_select2_params(args, limit=10)
        assert_that(result, equal_to({'search': None,
                                      'offset': 20,
                                      'limit': 10}))

    def test_build_select2_response_with_pagination(self):
        result = [{'key': 'value'}]
        total = 42
        params = {'search': 'a', 'offset': 10, 'limit': 10}
        response = build_select2_response(result, total, params)
        assert_that(response, equal_to({'results': result,
                                        'pagination': {'more': True}}))

    def test_build_select2_response_without_pagination(self):
        result = [{'key': 'value'}]
        total = 15
        params = {'search': 'a', 'offset': 10, 'limit': 10}
        response = build_select2_response(result, total, params)
        assert_that(response, equal_to({'results': result,
                                        'pagination': {'more': False}}))
