# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

from flask import render_template
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

    def get(self, id):
        conference = self.service.get(id)
        conference['extension'] = self._get_main_exten(conference['extensions'])
        form = ConferenceForm(data=conference)
        return render_template(self.templates['edit'], form=form, conference=conference)

    def _get_main_exten(self, extensions):
        for extension in extensions:
            return extension['exten']
        return None
