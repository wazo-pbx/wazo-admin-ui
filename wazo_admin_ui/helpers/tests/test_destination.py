# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import unittest

from hamcrest import assert_that, equal_to, empty

from ..destination import DestinationSchema


class TestDestinationSchema(unittest.TestCase):

    def setUp(self):
        self.schema = DestinationSchema()

    def test_post_dump(self):
        data = {'type': 'user',
                'user': {'user_id': 1,
                         'timeout': 2}}

        result = self.schema.dump(data).data
        assert_that(result, equal_to({'type': 'user',
                                      'user_id': 1,
                                      'timeout': 2}))

    def test_post_dump_with_csrf_token(self):
        data = {'type': 'user',
                'user': {'user_id': 1,
                         'timeout': 2,
                         'csrf_token': '123'}}

        result = self.schema.dump(data).data
        assert_that(result, equal_to({'type': 'user',
                                      'user_id': 1,
                                      'timeout': 2}))

    def test_post_dump_with_no_type(self):
        data = {}
        result = self.schema.dump(data).data
        assert_that(result, empty())

    def test_post_dump_with_no_destination_values(self):
        data = {'type': 'user'}
        result = self.schema.dump(data).data
        assert_that(result, empty())

    def test_post_dump_when_no_dict(self):
        data = []
        result = self.schema.dump(data).data
        assert_that(result, empty())

    def test_post_load(self):
        data = {'type': 'user',
                'user_id': 1,
                'timeout': 2}

        result = self.schema.load(data).data
        assert_that(result, equal_to({'type': 'user',
                                      'user': {'user_id': 1,
                                               'timeout': 2}}))

    def test_post_load_with_no_type(self):
        data = {}
        result = self.schema.load(data).data
        assert_that(result, empty())

    def test_post_load_with_no_destination_values(self):
        data = {'type': 'user'}
        result = self.schema.load(data).data
        assert_that(result, equal_to({'type': 'user',
                                      'user': {}}))
