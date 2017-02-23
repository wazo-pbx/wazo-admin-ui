# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_login import current_user
from xivo_confd_client import Client as ConfdClient


class BaseConfdService(object):
    resource = None
    confd_resource = None

    def __init__(self, confd_config):
        self.confd_config = confd_config

    @property
    def _confd(self):
        token = current_user.get_id()
        return ConfdClient(token=token, **self.confd_config)

    def list(self):
        resource_client = getattr(self._confd, self.confd_resource)
        return resource_client.list()

    def get(self, resource_id):
        resource_client = getattr(self._confd, self.confd_resource)
        return {self.resource: resource_client.get(resource_id)}

    def update(self, resources):
        resource_client = getattr(self._confd, self.confd_resource)
        resource = resources.get(self.resource)
        if not resource:
            return

        resource_client.update(resource)

    def create(self, resources):
        resource_client = getattr(self._confd, self.confd_resource)
        resource = resources.get(self.resource)
        if not resource:
            return

        resource_client.create(resource)

    def delete(self, resource_id):
        resource_client = getattr(self._confd, self.confd_resource)
        resource_client.delete(resource_id)
