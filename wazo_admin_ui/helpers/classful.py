# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import logging

from flask import (flash,
                   jsonify,
                   redirect,
                   render_template,
                   request,
                   url_for)
from flask_babel import gettext as _
from flask_classful import FlaskView
from flask_classful import route
from flask_login import login_required
from requests.exceptions import HTTPError

from wazo_admin_ui.helpers.error import ConfdErrorExtractor as e_extractor
from wazo_admin_ui.helpers.error import ErrorTranslator as e_translator
from wazo_admin_ui.helpers.destination import listing_urls

logger = logging.getLogger(__name__)

DEFAULT_TEMPLATE = '{blueprint}/{type_}.html'


def flash_basic_form_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash('{field} - {message}'.format(
                field=getattr(form, field).label.text,
                message=error
            ), 'error')


class LoginRequiredView(FlaskView):
    decorators = [login_required]


class IndexAjaxViewMixin(object):

    def _index(self, form=None):
        form = form or self.form()
        form = self._populate_form(form)

        return render_template(self._get_template('list'),
                               form=form,
                               resource_list=[],
                               listing_urls=listing_urls)

    def list_json(self):
        # TODO: handle case when flask return 302 because token is expired
        limit = request.args.get('length')
        if limit == '-1':
            limit = None

        offset = request.args.get('start')
        direction = request.args.get('order[0][dir]')
        order_column = request.args.get('order[0][column]', 0)
        order = request.args.get('columns[{}][data]'.format(order_column))
        search = request.args.get('search[value]')

        result = self.service.list(search=search, order=order, limit=limit, direction=direction, offset=offset)

        return jsonify({
            'recordsTotal': result['total'],
            'recordsFiltered': result.get('filtered', result['total']),
            'data': result['items']
        })


class NewViewMixin(object):

    def new(self):
        return self._new()

    def _new(self, form=None):
        form = form or self.form()
        return render_template(self._get_template('add'),
                               form=form)


class BaseView(LoginRequiredView):
    form = None
    resource = None
    service = None
    templates = {}

    def index(self):
        return self._index()

    def _index(self, form=None):
        try:
            resource_list = self.service.list()
        except HTTPError as error:
            self._flash_http_error(error)
            return redirect(url_for('admin.Admin:get'))

        form = form or self.form()
        form = self._populate_form(form)

        return render_template(self._get_template('list'),
                               form=form,
                               resource_list=resource_list,
                               listing_urls=listing_urls)

    def post(self):
        form = self.form()
        resources = self._map_form_to_resources_post(form)

        if not form.csrf_token.validate(form):
            flash_basic_form_errors(form)
            return self._new(form)

        try:
            self.service.create(resources)
        except HTTPError as error:
            form = self._fill_form_error(form, error)
            self._flash_http_error(error)
            return self._new(form)

        flash(_('%(resource)s: Resource has been created', resource=self.resource), 'success')
        return self._redirect_for('index')

    def _new(self, form=None):
        return self._index(form)

    def _map_form_to_resources_post(self, form):
        return self._map_form_to_resources(form)

    def get(self, id):
        return self._get(id)

    def _get(self, id, form=None):
        try:
            resource = self.service.get(id)
        except HTTPError as error:
            self._flash_http_error(error)
            return self._redirect_for('index')

        form = form or self._map_resources_to_form(resource)
        form = self._populate_form(form)

        return render_template(self._get_template('edit'),
                               form=form,
                               resource=resource,
                               listing_urls=listing_urls)

    def _map_resources_to_form(self, resource):
        return self.form(data=resource)

    def _populate_form(self, form):
        return form

    @route('/put/<id>', methods=['POST'])
    def put(self, id):
        form = self.form()
        if not form.csrf_token.validate(form):
            flash_basic_form_errors(form)
            return self._get(id, form)

        resources = self._map_form_to_resources_put(form, id)
        try:
            self.service.update(resources)
        except HTTPError as error:
            form = self._fill_form_error(form, error)
            self._flash_http_error(error)
            return self._get(id, form)

        flash(_('%(resource)s: Resource has been updated', resource=self.resource), 'success')
        return self._redirect_for('index')

    def _map_form_to_resources_put(self, form, form_id):
        return self._map_form_to_resources(form, form_id)

    def _map_form_to_resources(self, form, form_id=None):
        data = form.to_dict()
        if form_id:
            try:
                data['id'] = int(form_id)
            except ValueError:
                data['uuid'] = form_id
        return data

    def _map_resources_to_form_errors(self, form, resources):
        for resource in resources.values():
            form.populate_errors(resource)
            return form

    def _get_template(self, type_):
        return self.templates.get(type_, DEFAULT_TEMPLATE.format(blueprint=request.blueprint,
                                                                 type_=type_))

    @route('/delete/<id>', methods=['GET'])
    def delete(self, id):
        try:
            self.service.delete(id)
            flash(_('%(resource)s: Resource %(id)s has been deleted', resource=self.resource, id=id), 'success')
        except HTTPError as error:
            self._flash_http_error(error)

        return self._redirect_for('index')

    def _redirect_for(self, method_view):
        return redirect(url_for('.{}:{}'.format(self.__class__.__name__,
                                                method_view)))

    def _fill_form_error(self, form, error):
        response = error.response.json()
        error_id = e_extractor.extract_generic_error_id(response)
        if error_id == 'invalid-data':
            error_fields = e_extractor.extract_fields(response)
            error_field_ids = e_extractor.extract_specific_error_id_from_fields(error_fields)
            error_field_messages = e_translator.translate_specific_error_id_from_fields(error_field_ids)

            resource = e_extractor.extract_resource(error.request)
            form = self._map_resources_to_form_errors(form, {resource: error_field_messages})
        return form

    def _flash_http_error(self, error):
        response = error.response.json()
        resource = e_extractor.extract_resource(error.request)
        error_id = e_extractor.extract_generic_error_id(response)

        translated_resource = e_translator.resources.get(resource, '')
        flash('{resource}{delimiter}{generic_error}'.format(
            resource=translated_resource,
            delimiter=': ' if translated_resource else '',
            generic_error=e_translator.generic_messages.get(error_id, ''),
        ), 'error')
        flash('{method} {url}: {response}'.format(
            method=error.request.method,
            url=error.request.url,
            response=response,
        ), 'error_details')


def extract_select2_params(args, limit=10):
    search = args.get('term')
    page = args.get('page')

    if not _is_positive_integer(page):
        page = 1

    offset = (int(page) - 1) * limit
    return {'search': search,
            'offset': offset,
            'limit': limit}


def _is_positive_integer(value):
    if value is None:
        return False

    try:
        value = int(value)
    except ValueError:
        return False

    if value < 0:
        return False
    return True


def build_select2_response(results, total, params):
    return {'results': results,
            'pagination': {'more': (params['offset'] + params['limit']) < total}}
