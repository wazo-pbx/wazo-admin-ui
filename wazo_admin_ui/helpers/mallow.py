# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_wtf import FlaskForm
from marshmallow import Schema, fields, post_dump, pre_dump


class BaseSchema(Schema):
    _main_resource = None

    def on_bind_field(self, field_name, field_obj):
        field_obj.allow_none = True

    def get_attribute(self, attr, obj, default):
        if isinstance(obj, FlaskForm):
            value = getattr(obj, attr, default)
            return getattr(value, 'data', default)
        return super(BaseSchema, self).get_attribute(attr, obj, default)

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

            field_form.errors.append(value)
        return form

    @post_dump
    def add_main_resource_id(self, data):
        if self._main_resource:
            if self.context.get('resource_id'):
                data[self._main_resource]['id'] = self.context['resource_id']
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
