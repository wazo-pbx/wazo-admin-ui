# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import unittest

from hamcrest import assert_that, equal_to
from mock import Mock

from ..service import BaseConfdService


class TestBaseConfdService(unittest.TestCase):

    def setUp(self):
        self._resource1 = Mock()
        BaseConfdService.confd_resource = 'resource1'
        BaseConfdService.resource = 'resource1'
        BaseConfdService._confd = Mock(resource1=self._resource1)
        confd_config = {}
        self.service = BaseConfdService(confd_config)

    def test_list(self):
        self._resource1.list.return_value = [{'name': 'value'}]
        result = self.service.list()
        assert_that(result, equal_to([{'name': 'value'}]))

    def test_get(self):
        self._resource1.get.return_value = {'name': 'value'}
        result = self.service.get(42)
        assert_that(result, equal_to({'resource1': {'name': 'value'}}))

    def test_update(self):
        resources = {'resource1': {'name': 'value2'}}
        self.service.update(resources)
        self._resource1.update.assert_called_once_with({'name': 'value2'})

    def test_update_when_no_bad_resource(self):
        resources = {'bad_resource': {'name': 'value2'}}
        self.service.update(resources)
        self._resource1.update.assert_not_called()

    def test_create(self):
        resources = {'resource1': {'name': 'value2'}}
        self.service.create(resources)
        self._resource1.create.assert_called_once_with({'name': 'value2'})

    def test_create_when_bad_resource(self):
        resources = {'bad_resource': {'name': 'value2'}}
        self.service.create(resources)
        self._resource1.create.assert_not_called()

    def test_delete(self):
        self.service.delete(42)
        self._resource1.delete.assert_called_once_with(42)
