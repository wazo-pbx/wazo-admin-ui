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

    def _map_resources_to_form_get(self, conference):
        main_exten = self._get_main_exten(conference.get('extensions', {}))
        return self.form(data=conference, extension=main_exten)

    def _get_main_exten(self, extensions):
        for extension in extensions:
            return extension['exten']
        return None

    def _map_form_to_resources_post(self, form):
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

    def _map_form_to_resources_put(self, form, form_id):
        conference, extension = self.map_form_to_resources_post(form)
        conference['id'] = form_id
        conference['announce_only_user'] = form.announce_only_user.data
        conference['music_on_hold'] = form.music_on_hold.data
        conference['preprocess_subroutine'] = form.preprocess_subroutine.data
        conference['quiet_join_leave'] = form.quiet_join_leave.data
        return conference, extension

    def _map_resources_to_form_errors(self, form, resources):
        conference = resources.get('conferences')
        if conference:
            if 'name' in conference:
                form.name.errors.append(conference['name'])
            if 'pin' in conference:
                form.pin.errors.append(conference['pin'])
            if 'admin_pin' in conference:
                form.admin_pin.errors.append(conference['admin_pin'])
            if 'announce_join_leave' in conference:
                form.announce_join_leave.errors.append(conference['announce_join_leave'])
            if 'announce_user_count' in conference:
                form.announce_join_leave.errors.append(conference['announce_user_count'])
            if 'announce_only_user' in conference:
                form.announce_only_user.errors.append(conference['announce_only_user'])
            if 'music_on_hold' in conference:
                form.music_on_hold.errors.append(conference['music_on_hold'])
            if 'preprocess_subroutine' in conference:
                form.preprocess_subroutine.errors.append(conference['preprocess_subroutine'])
            if 'quiet_join_leave' in conference:
                form.quiet_join_leave.errors.append(conference['quiet_join_leave'])

        extension = resources.get('extensions')
        if extension:
            if 'exten' in extension:
                form.extension.errors.append(extension['exten'])

        return form
