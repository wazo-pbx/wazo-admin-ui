# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import unittest

from flask import Flask
from hamcrest import assert_that, equal_to, empty, has_entries
from wtforms import StringField, FormField, IntegerField

from ..destination import DestinationForm, FallbacksForm
from ..form import BaseForm


app = Flask('test_wazo_admin_ui')


class TestDestinationForm(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False

        class UserForm(BaseForm):
            user_id = IntegerField()
            timeout = StringField()

        DestinationForm.user = FormField(UserForm)

    def test_to_dict(self):
        data = {'type': 'user',
                'user-user_id': 1,
                'user-timeout': '2'}

        with app.test_request_context(method='POST', data=data):
            form = DestinationForm()
        result = form.to_dict()

        assert_that(result, equal_to({'type': 'user',
                                      'user_id': 1,
                                      'timeout': '2'}))

    def test_to_dict_with_no_type(self):
        data = {}

        with app.test_request_context(method='POST', data=data):
            form = DestinationForm()
        result = form.to_dict()

        assert_that(result, empty())

    def test_to_dict_with_no_destination_values(self):
        data = {'type': 'none'}

        with app.test_request_context(method='POST', data=data):
            form = DestinationForm()
        result = form.to_dict()

        assert_that(result, equal_to({'type': 'none'}))

    def test_to_dict_with_empty_string(self):
        data = {'type': 'user',
                'user-user_id': 1,
                'user-timeout': ''}

        with app.test_request_context(method='POST', data=data):
            form = DestinationForm()
        result = form.to_dict()

        assert_that(result, equal_to({'type': 'user',
                                      'user_id': 1,
                                      'timeout': None}))

    def test_process(self):
        data = {'type': 'user',
                'user-user_id': 1,
                'user-timeout': '2'}

        with app.test_request_context(method='POST', data=data):
            form = DestinationForm()

        assert_that(form.data, has_entries(type='user',
                                           user={'user_id': 1,
                                                 'timeout': '2'}))

    def test_process_with_no_type(self):
        data = {}

        with app.test_request_context(method='POST', data=data):
            form = DestinationForm()

        assert_that(form.data, has_entries(type='None'))

    def test_process_with_none_as_destination(self):
        data = {'type': 'none'}

        with app.test_request_context(method='POST', data=data):
            form = DestinationForm()

        assert_that(form.data, has_entries(type='none'))

    def test_process_with_kwargs(self):
        data = {'type': 'user',
                'user_id': 1,
                'timeout': '2'}

        with app.test_request_context():
            form = DestinationForm(**data)

        assert_that(form.data, has_entries(type='user',
                                           user={'user_id': 1,
                                                 'timeout': '2'}))

    def test_process_with_kwargs_and_undefined_form(self):
        data = {'type': 'queue',
                'queue_id': 1,
                'timeout': '2'}

        with app.test_request_context():
            form = DestinationForm(**data)

        assert_that(form.data, has_entries(type='queue',
                                           queue={'queue_id': 1,
                                                  'timeout': '2'}))

    def test_process_with_formdata(self):
        data = {'type': 'user',
                'user-user_id': 1,
                'user-timeout': '2'}

        with app.test_request_context(method='POST', data=data):
            form = DestinationForm()

        assert_that(form.data, has_entries(type='user',
                                           user={'user_id': 1,
                                                 'timeout': '2'}))

    def test_process_with_formdata_and_undefined_form(self):
        data = {'type': 'queue',
                'queue-queue_id': 1,
                'queue-timeout': '2'}

        with app.test_request_context(method='POST', data=data):
            form = DestinationForm()

        assert_that(form.data, has_entries(type='queue',
                                           queue={'queue_id': '1',
                                                  'timeout': '2'}))


class TestFallbacksForm(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False

    def test_to_dict_with_none_as_destination(self):
        data = {'busy_destination-type': 'none'}

        with app.test_request_context(method='POST', data=data):
            form = FallbacksForm()
        result = form.to_dict()

        assert_that(result, has_entries(busy_destination=None))
