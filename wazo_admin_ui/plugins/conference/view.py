# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

from flask_menu.classy import classy_menu_item

from wazo_admin_ui.helpers.classful import BaseView

from .form import ConferenceForm


class ConferenceView(BaseView):

    form = ConferenceForm
    resource = 'conference'
    templates = {'list': 'conferences.html',
                 'edit': 'view_conference.html'}

    @classy_menu_item('.conferences', 'Conferences', order=1, icon="compress")
    def index(self):
        return super(ConferenceView, self).index()

    def _serialize_get(self, conference):
        main_exten = self._get_main_exten(conference.get('extensions', {}))
        return self.form(data=conference, extension=main_exten)

    def _get_main_exten(self, extensions):
        for extension in extensions:
            return extension['exten']
        return None

    def _deserialize_post(self, form):
        conference = {
            'name': form.name.data,
            'announce_join_leave': form.announce_join_leave.data,
            'announce_user_count': form.announce_user_count.data,
            'pin': form.pin.data or None,
            'admin_pin': form.admin_pin.data or None
        }
        extension = {
            'exten': form.extension.data,
            'context': 'default'  # TODO: should be in the form
        }
        return conference, extension

    def _deserialize_put(self, conference_id, form):
        conference, extension = self._deserialize_post(form)
        conference['id'] = conference_id
        conference['announce_only_user'] = form.announce_only_user.data
        conference['music_on_hold'] = form.music_on_hold.data
        conference['preprocess_subroutine'] = form.preprocess_subroutine.data
        conference['quiet_join_leave'] = form.quiet_join_leave.data
        return conference, extension

    def map_errors(self, form, conferences=None, extensions=None):
        # TODO: Should be rework

        if conferences:
            if 'name' in conferences:
                form.name.errors.append(conferences['name'])
            if 'pin' in conferences:
                form.pin.errors.append(conferences['pin'])
            if 'admin_pin' in conferences:
                form.admin_pin.errors.append(conferences['admin_pin'])
            if 'announce_join_leave' in conferences:
                form.announce_join_leave.errors.append(conferences['announce_join_leave'])
            if 'announce_user_count' in conferences:
                form.announce_join_leave.errors.append(conferences['announce_user_count'])
            if 'announce_only_user' in conferences:
                form.announce_only_user.errors.append(conferences['announce_only_user'])
            if 'music_on_hold' in conferences:
                form.music_on_hold.errors.append(conferences['music_on_hold'])
            if 'preprocess_subroutine' in conferences:
                form.preprocess_subroutine.errors.append(conferences['preprocess_subroutine'])
            if 'quiet_join_leave' in conferences:
                form.quiet_join_leave.errors.append(conferences['quiet_join_leave'])

        if extensions:
            if 'exten' in extensions:
                form.extension.errors.append(extensions['exten'])

        return form
