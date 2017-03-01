# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import unittest
from mock import Mock
from flask_wtf import FlaskForm

from hamcrest import assert_that, contains, empty
from marshmallow import fields

from ..classful import BaseView
from ..error import ErrorExtractor
from ..error import ErrorTranslator
from ..mallow import BaseSchema, BaseAggregatorSchema

SINGULARIZE_RESOURCES = {'resources_plurial': 'resource'}

GENERIC_PATTERN_ERRORS = {'invalid-data': r'^Input Error'}
GENERIC_MESSAGE_ERRORS = {'invalid-data': 'Input Error'}

SPECIFIC_PATTERN_ERRORS = {'invalid-length': r'Longer than maximum length'}
SPECIFIC_MESSAGE_ERRORS = {'invalid-length': 'Longer than maximum length'}


class ResourceSchema(BaseSchema):

    class Meta:
        fields = ('attribute1', 'attribute2')


class AggregatorSchema(BaseAggregatorSchema):
    _main_resource = 'resource'

    resource = fields.Nested(ResourceSchema)


class TestBaseView(unittest.TestCase):

    def setUp(self):
        self.view = BaseView()
        self.view.schema = AggregatorSchema
        ErrorExtractor.generic_patterns = GENERIC_PATTERN_ERRORS
        ErrorExtractor.specific_patterns = SPECIFIC_PATTERN_ERRORS
        ErrorExtractor.singularize_resources = SINGULARIZE_RESOURCES
        ErrorTranslator.generic_messages = GENERIC_MESSAGE_ERRORS
        ErrorTranslator.specific_messages = SPECIFIC_MESSAGE_ERRORS

        self.form = Mock(FlaskForm,
                         attribute1=Mock(data='value1', errors=[], raw_data='value1'))

    def test_fill_form_error_with_confd_input_error(self):
        confd_error = ["Input Error - attribute1: 'Longer than maximum length'"]
        path_url = '/1.1/resources_plurial/42'
        form = self.view._fill_form_error(self.form, self._build_error(confd_error, path_url))

        assert_that(form.attribute1.errors, contains('Longer than maximum length'))

    def test_fill_form_error_with_confd_input_error_and_not_register_msg(self):
        confd_error = ["Input Error - attribute1: 'Unregistered message'"]
        path_url = '/1.1/resources_plurial/42'
        form = self.view._fill_form_error(self.form, self._build_error(confd_error, path_url))

        assert_that(form.attribute1.errors, empty())

    def test_fill_form_error_with_confd_input_error_and_invalid_attribute(self):
        confd_error = ["Input Error - invalid_attr: 'Longer than maximum length'"]
        path_url = '/1.1/resources_plurial/42'
        form = self.view._fill_form_error(self.form, self._build_error(confd_error, path_url))

        assert_that(form.attribute1.errors, empty())

    def test_fill_form_error_with_confd_input_error_and_invalid_format(self):
        confd_error = ["Input Error - field 'users': User was not found ('uuid': 'patate')"]
        path_url = '/1.1/resources_plurial/42'
        form = self.view._fill_form_error(self.form, self._build_error(confd_error, path_url))

        assert_that(form.attribute1.errors, empty())

    def test_fill_form_error_with_confd_not_input_error(self):
        confd_error = ["Some Error - "]
        path_url = '/1.1/resources_plurial/42'
        form = self.view._fill_form_error(self.form, self._build_error(confd_error, path_url))

        assert_that(form.attribute1.errors, empty())

    def test_fill_form_error_with_confd_input_error_with_unregistered_resource(self):
        confd_error = ["Input Error - attribute1: 'Longer than maximum length'"]
        path_url = '/1.1/unregistered_resource/42'
        form = self.view._fill_form_error(self.form, self._build_error(confd_error, path_url))

        assert_that(form.attribute1.errors, empty())

    def _build_error(self, error, path_url):
        return Mock(response=Mock(json=Mock(return_value=error)),
                    request=Mock(path_url=path_url))
