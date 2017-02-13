# -*- coding: utf-8 -*-
# Copyright 2017 by Sylvain Boily
# SPDX-License-Identifier: GPL-3.0+

from flask_login import current_user
from xivo_confd_client import Client as ConfdClient


class ConferenceService(object):

    def __init__(self, confd_config):
        self.confd_config = confd_config

    @property
    def _confd(self):
        token = current_user.get_id()
        return ConfdClient(token=token, **self.confd_config)

    def list(self):
        return self._confd.conferences.list()

    def get(self, conference_id):
        return self._confd.conferences.get(conference_id)

    def update(self, conference, extension):
        existing_extension = self._get_main_extension(conference['id'])

        self._confd.conferences.update(conference)

        if not extension:
            return

        if extension['exten'] and existing_extension:
            self._update_extension(existing_extension, extension)
        elif extension['exten']:
            self._add_extension(conference['id'], extension)
        elif not extension['exten'] and existing_extension:
            self._remove_extension(conference['id'], extension['id'])

    def _get_main_extension(self, conference_id):
        for extension in self._confd.conferences.get(conference_id)['extensions']:
            return extension
        return None

    def create(self, conference, extension):
        conference = self._confd.conferences.create(conference)
        if conference and extension:
            self._add_extension(conference['id'], extension)

    def delete(self, conference_id):
        conference = self._confd.conferences.get(conference_id)
        for extension in conference['extensions']:
            self._remove_extension(conference_id, extension['id'])
        self._confd.conferences.delete(conference_id)

    def _update_extension(self, existing_extension, extension):
        if existing_extension['exten'] == extension['exten']:
            return

        extension['id'] = existing_extension['id']
        self._confd.extensions.update(extension)

    def _add_extension(self, conference_id, extension):
        extension = self._confd.extensions.create(extension)
        if extension:
            self._confd.conferences(conference_id).add_extension(extension)

    def _remove_extension(self, conference_id, extension_id):
        self._confd.conferences(conference_id).remove_extension(extension_id)
        self._confd.extensions.delete(extension_id)
