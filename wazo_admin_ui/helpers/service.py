# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import logging

from flask_login import current_user
from xivo_confd_client import Client as ConfdClient

logger = logging.getLogger(__name__)


class BaseConfdService(object):
    resource_name = None
    resource_confd = None

    def __init__(self, confd_config):
        self.confd_config = confd_config

    @property
    def _confd(self):
        token = current_user.get_id()
        return ConfdClient(token=token, **self.confd_config)

    def list(self, limit=None, order=None, direction=None, offset=None, search=None, **kwargs):
        resource_client = getattr(self._confd, self.resource_confd)
        return resource_client.list(search=search,
                                    order=order,
                                    limit=limit,
                                    direction=direction,
                                    offset=offset,
                                    **kwargs)

    def get(self, resource_id):
        resource_client = getattr(self._confd, self.resource_confd)
        return {self.resource_name: resource_client.get(resource_id)}

    def update(self, resources):
        resource = resources.get(self.resource_name)
        if not resource:
            return

        resource_client = getattr(self._confd, self.resource_confd)
        resource_client.update(resource)

    def create(self, resources):
        resource = resources.get(self.resource_name)
        if not resource:
            return

        resource_client = getattr(self._confd, self.resource_confd)
        return resource_client.create(resource)

    def delete(self, resource_id):
        resource_client = getattr(self._confd, self.resource_confd)
        resource_client.delete(resource_id)


class BaseConfdExtensionService(BaseConfdService):

    def _extract_resource_extension(self, resources):
        resource = resources.get(self.resource_name)
        extension = resources.get('extension')
        if not resource or not extension:
            logger.debug('Missing %s or extension resource', self.resource_confd)
            return
        return resource, extension

    def create(self, resources):
        resource = super(BaseConfdExtensionService, self).create(resources)
        _, extension = self._extract_resource_extension(resources)
        self.create_extension(extension, resource)
        return resource

    def update(self, resources):
        super(BaseConfdExtensionService, self).update(resources)
        resource, extension = self._extract_resource_extension(resources)
        self.update_extension(extension, resource)

    def delete(self, resource_id):
        self.delete_extension(resource_id)
        super(BaseConfdExtensionService, self).delete(resource_id)

    def create_extension(self, extension, resource):
        if resource and extension:
            if extension.get('exten') and extension.get('context'):
                self._add_extension(extension, resource)

    def update_extension(self, extension, resource):
        if not extension or not resource:
            return

        existing_extension = self._get_main_extension(resource)

        if extension.get('exten') and existing_extension:
            self._update_extension(extension, existing_extension)

        elif extension.get('exten'):
            self._add_extension(extension, resource)

        elif not extension.get('exten') and existing_extension:
            self._remove_extension(existing_extension, resource)

    def delete_extension(self, resource_id):
        resource_client = getattr(self._confd, self.resource_confd)
        resource = resource_client.get(resource_id)
        for extension in resource['extensions']:
            self._remove_extension(extension, resource)

    def _add_extension(self, extension, resource):
        extension = self._confd.extensions.create(extension)
        if extension:
            resource_client = getattr(self._confd, self.resource_confd)
            resource_client(resource).add_extension(extension)

    def _update_extension(self, extension, existing_extension):
        if existing_extension.get('exten') == extension.get('exten') and \
           existing_extension.get('context') == extension.get('context'):
            return

        extension['id'] = existing_extension['id']
        self._confd.extensions.update(extension)

    def _remove_extension(self, extension, resource):
        resource_client = getattr(self._confd, self.resource_confd)
        resource_client(resource).remove_extension(extension)
        self._confd.extensions.delete(extension)

    def _get_main_extension(self, resource):
        resource_id = resource.get('uuid', resource.get('id'))
        if not resource_id:
            logger.debug('Unable to extract resource_id from %s resource', self.resource_confd)
            return

        resource_client = getattr(self._confd, self.resource_confd)
        for extension in resource_client.get(resource_id)['extensions']:
            return extension
        return None
