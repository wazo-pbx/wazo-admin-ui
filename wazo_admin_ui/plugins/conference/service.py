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

    def view(self, id):
        return self._confd.conferences.get(id)

    def update(self, id, conference, extension):
        update_conference = {
            'id': id,
            'name': conference.name.data,
            'announce_join_leave': conference.announce_join_leave.data,
            'announce_user_count': conference.announce_user_count.data,
            'announce_only_user': conference.announce_only_user.data,
            'music_on_hold': conference.music_on_hold.data,
            'preprocess_subroutine': conference.preprocess_subroutine.data,
            'quiet_join_leave': conference.quiet_join_leave.data,
            'pin': conference.pin.data or None,
            'admin_pin': conference.admin_pin.data or None
        }

        self._confd.conferences.update(update_conference)

        if conference.extension.data and extension:
            self.update_extension(extension, conference.extension.data, id)
        elif conference.extension.data:
            self.add_extension(conference.extension.data, id)
        elif not conference.extension.data and extension:
            self.remove_extension(extension['id'], id)

    def add(self, conference):
        create_conference = {
            'name': conference.name.data,
            'announce_join_leave': conference.announce_join_leave.data,
            'announce_user_count': conference.announce_user_count.data,
            'pin': conference.pin.data or None,
            'admin_pin': conference.admin_pin.data or None
        }

        cnf = self._confd.conferences.create(create_conference)
        if conference.extension.data and cnf:
            self.add_extension(conference.extension.data, cnf['id'])

    def add_extension(self, exten, conference_id):
        search_extension = self._confd.extensions.list(exten=exten, context='default')['items']
        if len(search_extension) == 0:
            create_extension = {
                'exten': exten,
                'context': 'default'
            }
            extension = self._confd.extensions.create(create_extension)
            if extension:
                self._confd.conferences.relations(conference_id).add_extension(extension)

    def update_extension(self, extension, new_exten, conference_id):
        old_extension = extension['exten']
        exten_id = extension['id']
        if new_exten != old_extension:
            search_extension = self._confd.extensions.list(exten=new_exten, context='default')['items']
            if len(search_extension) == 0:
                update_extension = {
                    'id': exten_id,
                    'exten': new_exten,
                    'context': 'default'
                }
                self._confd.extensions.update(update_extension)

    def remove_extension(self, exten_id, conference_id):
        self._confd.conferences.relations(conference_id).remove_extension(exten_id)
        self._confd.extensions.delete(exten_id)

    def remove(self, conference_id):
        conference = self._confd.conferences.get(conference_id)
        if conference.has_key('extensions'):
            for exten in conference['extensions']:
                self.remove_extension(exten['id'], conference_id)
        self._confd.conferences.delete(conference_id)
