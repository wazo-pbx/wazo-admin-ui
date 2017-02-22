# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import unittest
from mock import Mock
from marshmallow import fields, pre_dump
from flask_wtf import FlaskForm

from hamcrest import assert_that, contains, empty, equal_to, has_entries, has_properties

from ..mallow import BaseSchema


class Resource1Schema(BaseSchema):

    class Meta:
        additional = ('attribute1', 'attribute2')


class Resource2Schema(BaseSchema):

    attribute1 = fields.String(attribute='attribute3')
    attribute4 = fields.String(default='default_value4')


class ResourceFormSchema(BaseSchema):
    _main_resource = 'resource1'

    resource1 = fields.Nested(Resource1Schema)
    resource2 = fields.Nested(Resource2Schema)

    @pre_dump
    def add_envelope(self, data):
        return {'resource1': data,
                'resource2': data}


class TestBaseSchema(unittest.TestCase):

    def setUp(self):
        self.schema = ResourceFormSchema

    def test_get_attribute(self):
        form = Mock(FlaskForm,
                    attribute1=Mock(data='value1'),
                    attribute2=Mock(data='value2'),
                    attribute3=Mock(data='value3'))

        resources = self.schema().dump(form).data

        assert_that(resources, has_entries(resource1=has_entries(attribute1='value1',
                                                                 attribute2='value2'),
                                           resource2=has_entries(attribute1='value3',
                                                                 attribute4='default_value4')))

    def test_populate_form_errors(self):
        form = Mock(FlaskForm,
                    attribute1=Mock(errors=[]),
                    attribute2=Mock(errors=[]),
                    attribute3=Mock(errors=[]),
                    attribute4=Mock(errors=[]))

        resources_errors = {'resource1': {'attribute1': 'error1',
                                          'attribute2': 'error2'},
                            'resource2': {'attribute1': 'error3',
                                          'attribute4': 'error4'}}
        form = self.schema().populate_form_errors(form, resources_errors)

        assert_that(form, has_properties(
            attribute1=has_properties(errors=contains('error1')),
            attribute2=has_properties(errors=contains('error2')),
            attribute3=has_properties(errors=contains('error3')),
            attribute4=has_properties(errors=contains('error4')),
        ))

    def test_add_main_resource_id(self):
        form = Mock(FlaskForm,
                    attribute1=Mock(data='value1'),
                    attribute2=Mock(data='value2'))

        resources = self.schema(context={'resource_id': 54}).dump(form).data

        assert_that(resources, has_entries(resource1=has_entries(id=54)))

    def test_get_main_exten(self):
        extensions = [{'exten': '1234'}, {'exten': '5678'}]

        main_exten = self.schema().get_main_exten(extensions)

        assert_that(main_exten, equal_to('1234'))

    def test_on_bind_field_set_allow_none_true(self):
        resources = {'resource1': {'attribute1': None}}

        _, errors = self.schema().load(resources)

        assert_that(errors, empty())
