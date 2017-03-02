# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_wtf import FlaskForm
from marshmallow import Schema, fields, post_dump, pre_dump
from marshmallow.utils import missing


def extract_form_fields(form):
    # Based on wtform code
    result = []
    for name in dir(form):
        if not name.startswith('_') and name != 'submit':
            unbound_field = getattr(form, name)
            if hasattr(unbound_field, '_formfield'):
                result.append(name)
    return result


class BaseSchema(Schema):
    _main_resource = None

    def on_bind_field(self, field_name, field_obj):
        field_obj.allow_none = True

    def get_attribute(self, attr, obj, default):
        if isinstance(obj, FlaskForm):
            value = getattr(obj, attr, default)
            if not self._data_is_given_in_input(value):
                return missing

            result = getattr(value, 'data', default)
            return result if result != '' else None
        return super(BaseSchema, self).get_attribute(attr, obj, default)

    def _data_is_given_in_input(self, obj):
        try:
            raw_data = getattr(obj, 'raw_data')
        except AttributeError:
            return False

        return len(raw_data) != 0

    def populate_form_errors(self, form, resources):
        for field_name, value in resources.iteritems():
            field_obj = self.fields.get(field_name, None)
            if not field_obj:
                continue

            if isinstance(field_obj, fields.Nested):
                form = field_obj.schema.populate_form_errors(form, value)
                continue

            attribute = field_obj.attribute if field_obj.attribute else field_name
            field_form = getattr(form, attribute, None)
            if not field_form:
                continue

            # normally it's form.validate() that make this conversion
            field_form.errors = list(field_form.errors)

            field_form.errors.append(value)
        return form

    @post_dump
    def add_main_resource_id(self, data):
        if self._main_resource:
            resource_id = self.context.get('resource_id')
            if resource_id:
                try:
                    data[self._main_resource]['id'] = int(resource_id)
                except ValueError:
                    data[self._main_resource]['uuid'] = resource_id
        return data

    def get_main_exten(self, extensions):
        for extension in extensions:
            return extension['exten']
        return None


class BaseAggregatorSchema(BaseSchema):

    @pre_dump
    def add_envelope(self, data):
        result = {}
        for field in self.fields:
            result[field] = data
        return result
