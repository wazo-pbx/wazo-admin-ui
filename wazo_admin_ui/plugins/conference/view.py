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
        main_exten = self._get_main_exten(conference['extensions'])
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
