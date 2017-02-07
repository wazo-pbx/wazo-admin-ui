# -*- coding: utf-8 -*-
# Copyright 2017 by Sylvain Boily
# SPDX-License-Identifier: GPL-3.0+

import logging

from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash

from flask_classful import FlaskView
from flask_classful import route
from flask_menu.classy import classy_menu_item
from flask_login import login_required

from wazo_admin_ui.core.errors import flash_errors

from .services import ServiceConferences
from .forms import FormConference

logger = logging.getLogger(__name__)

class Conferences(FlaskView):
    decorators = [login_required]

    @classy_menu_item('.conferences', 'Conferences', order=1, icon="compress")
    def get(self):
        try:
            c = ServiceConferences()
            conferences = c.list()
            form = FormConference()
            return render_template('conferences.html', conferences=conferences, form=form)
        except Exception as e:
            flash(u'There is a problem to get your conferences: {}'.format(e), 'error')
        return redirect(url_for('admin.Admin:get'))

    def post(self):
        form = FormConference()

        if form.validate_on_submit():
            try:
                c = ServiceConferences()
                c.add(form)
                flash(u'Conference {} has been created'.format(form.name.data), 'success')
            except Exception as e:
                flash(u'Conference {} has not been created: {}'.format(form.name.data, e), 'error')
        else:
            flash_errors(form)
        return redirect(url_for('conference.Conferences:get'))

    @route('/view/<id>', methods=['GET', 'POST'])
    def view(self, id):
        c = ServiceConferences()
        conference = c.view(id)
        extension = None
        if len(conference['extensions']) > 0:
            extension = conference['extensions'][0]
            conference['extension'] = extension['exten']
        form = FormConference(data=conference)

        if form.validate_on_submit():
            try:
                c.update(id, form, extension)
                flash(u'Conference {} has been updated'.format(form.name.data), 'success')
                return redirect(url_for('conference.Conferences:get'))
            except Exception as e:
                flash(u'Conference {} has not been updated: {}'.format(form.name.data, e), 'error')
        else:
            flash_errors(form)

        return render_template('view_conference.html', form=form, conference=conference)

    def remove(self, id):
        try :
            c = ServiceConferences()
            c.remove(id)
            flash(u'Conference {} has been deleted'.format(id), 'success')
        except Exception as e:
            flash(u'Conference {} has not been deleted: {}'.format(id, e), 'error')
        return redirect(url_for('conference.Conferences:get'))
