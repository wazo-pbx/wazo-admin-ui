# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

from flask import render_template
from flask import redirect
from flask import url_for
from flask import flash
from flask_classful import FlaskView
from flask_classful import route
from flask_login import login_required
from requests.exceptions import HTTPError

from wazo_admin_ui.helpers.error import ConfdErrorExtractor as e_extractor
from wazo_admin_ui.helpers.error import ErrorTranslator as e_translator


def flash_basic_form_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash('Error in the {field} field - {message}'.format(
                field=getattr(form, field).label.text,
                message=error
            ), 'error')


class LoginRequiredView(FlaskView):
    decorators = [login_required]


class BaseView(LoginRequiredView):
    form = None
    resource = None
    service = None
    templates = {'list': None,
                 'edit': None,
                 'create': None}

    def index(self):
        return self._index()

    def _index(self, form=None):
        try:
            result = self.service.list()
        except HTTPError as error:
            self._flash_http_error(error)
            return redirect(url_for('admin.Admin:get'))

        form = form or self.form()
        return render_template(self.templates['list'], form=form, result=result)

    def post(self):
        form = self.form()

        if not form.validate_on_submit():
            flash_basic_form_errors(form)
            return self._index(form)

        resources = self.map_form_to_resources_post(form)
        try:
            self.service.create(*resources)
        except HTTPError as error:
            form = self._fill_form_error(form, error)
            self._flash_http_error(error)
            return self._index(form)

        flash('{} has been created'.format(self.resource), 'success')
        return self._redirect_for('index')

    def map_form_to_resources_post(self, form):
        return (form.data,)

    def get(self, id):
        return self._get(id)

    def _get(self, id, form=None):
        try:
            result = self.service.get(id)
        except HTTPError as error:
            self._flash_http_error(error)
            return self._redirect_for('index')

        form = form or self.map_resources_to_form_get(result)
        return render_template(self.templates['edit'], form=form, result=result)

    def map_resources_to_form_get(self, obj):
        return self.form(data=obj)

    @route('/put/<id>', methods=['POST'])
    def put(self, id):
        form = self.form()
        if not form.validate_on_submit():
            flash_basic_form_errors(form)
            return self._get(id, form)

        resources = self.map_form_to_resources_put(form, id)
        try:
            self.service.update(*resources)
        except HTTPError as error:
            form = self._fill_form_error(form, error)
            self._flash_http_error(error)
            return self._get(id, form)

        flash(u'{} has been updated'.format(self.resource), 'success')
        return self._redirect_for('index')

    def map_form_to_resources_put(form_id, form):
        result = form.data
        result['id'] = form_id
        return (result,)

    def map_resources_to_form_errors(form, resources):
        pass

    @route('/delete/<id>', methods=['GET'])
    def delete(self, id):
        try:
            self.service.delete(id)
            flash(u'{} {} has been deleted'.format(self.resource, id), 'success')
        except HTTPError as error:
            self._flash_http_error(error)

        return self._redirect_for('index')

    def _redirect_for(self, method_view):
        return redirect(url_for('{}.{}:{}'.format(self.get_route_base(),
                                                  self.__class__.__name__,
                                                  method_view)))

    def _fill_form_error(self, form, error):
        response = error.response.json()
        resource = e_extractor.extract_resource(error.request)
        error_id = e_extractor.extract_generic_error_id(response)
        if error_id == 'invalid-data':
            error_fields = e_extractor.extract_fields(response)
            error_field_ids = e_extractor.extract_specific_error_id_from_fields(error_fields)
            error_field_messages = e_translator.translate_specific_error_id_from_fields(error_field_ids)
            form = self.map_resources_to_form_errors(form, {resource: error_field_messages})
        return form

    def _flash_http_error(self, error):
        response = error.response.json()
        resource = e_extractor.extract_resource(error.request)
        error_id = e_extractor.extract_generic_error_id(response)

        flash('{resource}: {generic_error}'.format(
            resource=e_translator.resources.get(resource, ''),
            generic_error=e_translator.generic_messages.get(error_id, ''),
        ), 'error')
        flash('{method} {url}: {response}'.format(
            method=error.request.method,
            url=error.request.url,
            response=response,
        ), 'error_details')
