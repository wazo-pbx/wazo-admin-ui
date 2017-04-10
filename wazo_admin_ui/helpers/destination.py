# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from marshmallow import fields, post_load, post_dump
from wtforms.fields import SelectField, FormField, HiddenField
from wtforms.utils import unset_value

from wazo_admin_ui.helpers.mallow import BaseSchema
from .form import BaseForm


_destination_choices = set()
listing_urls = {}


def register_listing_url(type_id, endpoint):
    listing_urls[type_id] = endpoint


def register_destination_form(type_id, type_label, form):
    _destination_choices.add((type_id, type_label))
    setattr(DestinationForm, type_id, FormField(form))


class DestinationForm(BaseForm):

    type = SelectField('Destination', choices=[])

    def __init__(self, *args, **kwargs):
        super(DestinationForm, self).__init__(*args, **kwargs)
        self.type.choices = [('none', 'None')] + list(_destination_choices)
        self.listing_urls = listing_urls

    def to_dict(self):
        data = super(DestinationForm, self).to_dict()

        destination_type = data.get('type')
        if not destination_type:
            return {}

        destination = data.get(destination_type, {})
        result = self._convert_all_empty_string_to_none(destination)
        result['type'] = destination_type
        return result

    def _convert_all_empty_string_to_none(self, data):
        result = {}
        for key, val in data.iteritems():
            result[key] = val if val != '' else None
        return result

    def process(self, formdata=None, obj=None, data=None, **kwargs):
        destination = kwargs
        if destination and 'type' in destination:
            destination_type = destination.pop('type')
            kwargs = {'type': destination_type,
                      destination_type: kwargs}

        super(DestinationForm, self).process(formdata, obj, data, **kwargs)


class DestinationField(FormField):

    def __init__(self, *args, **kwargs):
        self.destination_label = kwargs.pop('destination_label', None)
        super(DestinationField, self).__init__(DestinationForm, *args, **kwargs)

    def process(self, formdata, data=unset_value):
        super(DestinationField, self).process(formdata, data)
        if self.destination_label is not None:
            self.form.type.label.text = self.destination_label


class FallbacksForm(BaseForm):
    busy_destination = DestinationField('Busy')
    congestion_destination = DestinationField('Congestion')
    fail_destination = DestinationField('Fail')
    noanswer_destination = DestinationField('No answer')

    def to_dict(self):
        data = super(FallbacksForm, self).to_dict()

        for key, val in data.iteritems():
            if val.get('type') == 'none':
                data[key] = None
        return data


class DestinationHiddenField(HiddenField):

    def __init__(self, *args, **kwargs):
        def remove_none(value):
            return value or ''
        super(DestinationHiddenField, self).__init__(filters=[remove_none], *args, **kwargs)


class DestinationSchema(BaseSchema):

    @post_dump(pass_original=True)
    def _dump_dynamic_destination(self, data, raw_data):
        if not isinstance(raw_data, dict):
            return {}

        destination_type = raw_data.get('type')
        if not destination_type:
            return {}

        destination = raw_data.get(destination_type, {})
        result = self._convert_all_empty_string_to_none(destination)

        result['type'] = destination_type
        result.pop('csrf_token', None)
        return result

    @post_load(pass_original=True)
    def _load_dynamic_destination(self, data, raw_data):
        if not isinstance(raw_data, dict):
            return {}

        destination_type = raw_data.pop('type', None)
        if not destination_type:
            return {}

        result = {'type': destination_type,
                  destination_type: raw_data}
        return result

    def _convert_all_empty_string_to_none(self, data):
        result = {}
        for key, val in data.iteritems():
            result[key] = val if val != '' else None
        return result


class FallbacksSchema(BaseSchema):
    busy_destination = fields.Nested(DestinationSchema)
    congestion_destination = fields.Nested(DestinationSchema)
    fail_destination = fields.Nested(DestinationSchema)
    noanswer_destination = fields.Nested(DestinationSchema)

    @post_dump
    def _set_empty_fallback_to_none(self, data):
        for key, value in data.iteritems():
            if not value or value.get('type') == 'none':
                data[key] = None
        return data
