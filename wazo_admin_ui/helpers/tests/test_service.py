# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import unittest

from hamcrest import assert_that, equal_to
from mock import Mock

import wazo_admin_ui.helpers.service
from ..service import BaseConfdService, BaseConfdExtensionService


class TestBaseConfdService(unittest.TestCase):

    def setUp(self):
        self._resource1 = Mock()
        BaseConfdService.resource_confd = 'resource1'
        BaseConfdService.resource_name = 'resource1'
        wazo_admin_ui.helpers.service.confd = Mock(resource1=self._resource1)
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


class TestBaseConfdExtensionService(unittest.TestCase):

    def setUp(self):
        self._resource1 = Mock()
        self._extensions = Mock()
        BaseConfdService.resource_confd = 'resource1'
        BaseConfdService.resource_name = 'resource1'
        wazo_admin_ui.helpers.service.confd = Mock(resource1=self._resource1,
                                                   extensions=self._extensions)
        confd_config = {}
        self.service = BaseConfdExtensionService(confd_config)

    def _assert_no_confd_call(self):
        self._extensions.create.assert_not_called()
        self._extensions.update.assert_not_called()
        self._extensions.delete.assert_not_called()
        self._resource1.assert_not_called()
        self._resource1.return_value.remove_extension.assert_not_called()
        self._resource1.return_value.add_extension.assert_not_called()

    def test_update_extension_when_no_extension(self):
        resource = {'id': 3}
        extension = None
        self.service.update_extension(extension, resource)
        self._assert_no_confd_call()

    def test_update_extension_when_no_resource(self):
        resource = {'id': 3}
        extension = None
        self.service.update_extension(extension, resource)
        self._assert_no_confd_call()

    def test_update_extension_when_extension_is_empty(self):
        resource = {'id': 3}
        extension = {}
        self.service.update_extension(extension, resource)
        self._assert_no_confd_call()

    def test_update_extension_when_exten_is_removed(self):
        existing_extension = {'exten': None, 'context': 'default', 'id': 42}
        self._resource1.get.return_value = {'extensions': [existing_extension]}
        resource = {'id': 3}
        extension = {'exten': None, 'context': 'default'}
        self.service.update_extension(extension, resource)

        self._extensions.delete.assert_called_once_with(existing_extension)
        self._resource1.assert_called_once_with(resource)
        self._resource1.return_value.remove_extension.assert_called_once_with(existing_extension)

    def test_update_extension_when_no_exten_key(self):
        existing_extension = {'exten': None, 'context': 'default', 'id': 42}
        self._resource1.get.return_value = {'extensions': [existing_extension]}
        resource = {'id': 3}
        extension = {'context': 'default'}
        self.service.update_extension(extension, resource)

        self._extensions.delete.assert_called_once_with(existing_extension)
        self._resource1.assert_called_once_with(resource)
        self._resource1.return_value.remove_extension.assert_called_once_with(existing_extension)

    def test_update_extension_when_no_exten_and_no_existing_extension(self):
        self._resource1.get.return_value = {'extensions': []}
        resource = {'id': 3}
        extension = {'exten': None, 'context': 'default'}
        self.service.update_extension(extension, resource)
        self._assert_no_confd_call()

    def test_update_extension_when_same_extension_and_existing_extension(self):
        exten, context = '123', 'default'
        existing_extension = {'exten': exten, 'context': context, 'id': 42}
        self._resource1.get.return_value = {'extensions': [existing_extension]}
        resource = {'id': 3}
        extension = {'exten': exten, 'context': context}
        self.service.update_extension(extension, resource)
        self._assert_no_confd_call()

    def test_update_extension_when_different_extension_and_existing_extension(self):
        existing_extension = {'exten': '123', 'context': 'default', 'id': 42}
        self._resource1.get.return_value = {'extensions': [existing_extension]}
        resource = {'id': 3}
        extension = {'exten': '456', 'context': 'default'}
        self.service.update_extension(extension, resource)

        expected_call = extension
        expected_call['id'] = 42
        self._extensions.update.assert_called_once_with(expected_call)

    def test_update_extension_when_extension_and_no_existing_extension(self):
        self._resource1.get.return_value = {'extensions': []}
        resource = {'id': 3}
        extension = {'exten': '456', 'context': 'default'}
        self._extensions.create.return_value = extension

        self.service.update_extension(extension, resource)

        self._extensions.create.assert_called_once_with(extension)
        self._resource1.assert_called_once_with(resource)
        self._resource1.return_value.add_extension.assert_called_once_with(extension)

    def test_create_extension_when_no_extension(self):
        resource = {'id': 3}
        extension = None
        self.service.create_extension(extension, resource)
        self._assert_no_confd_call()

    def test_create_extension_when_no_resource(self):
        resource = {'id': 3}
        extension = None
        self.service.create_extension(extension, resource)
        self._assert_no_confd_call()

    def test_create_extension_when_extension_is_empty(self):
        resource = {'id': 3}
        extension = {}
        self.service.create_extension(extension, resource)
        self._assert_no_confd_call()

    def test_create_extension_when_exten_is_None(self):
        resource = {'id': 3}
        extension = {'exten': None, 'context': 'default'}
        self.service.create_extension(extension, resource)
        self._assert_no_confd_call()

    def test_create_extension_when_context_is_None(self):
        resource = {'id': 3}
        extension = {'exten': '123', 'context': None}
        self.service.create_extension(extension, resource)
        self._assert_no_confd_call()

    def test_create_extension_when_extension_and_resource(self):
        resource = {'id': 3}
        extension = {'exten': '1234', 'context': 'default'}
        self._extensions.create.return_value = extension

        self.service.create_extension(extension, resource)

        self._extensions.create.assert_called_once_with(extension)
        self._resource1.assert_called_once_with(resource)
        self._resource1.return_value.add_extension.assert_called_once_with(extension)

    def test_delete_extension_when_no_extension(self):
        resource = {'id': 42, 'extensions': []}
        self._resource1.get.return_value = resource
        self.service.delete_extension(resource['id'])
        self._assert_no_confd_call()

    def test_delete_extension_when_extension_and_resource(self):
        extension = {'id': 1, 'exten': '1234', 'context': 'default'}
        resource = {'id': 42, 'extensions': [extension]}
        self._resource1.get.return_value = resource

        self.service.delete_extension(resource['id'])

        self._extensions.delete.assert_called_once_with(extension)
        self._resource1.assert_called_once_with(resource)
        self._resource1.return_value.remove_extension.assert_called_once_with(extension)
