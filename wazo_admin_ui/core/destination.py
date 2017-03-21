# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_wtf import FlaskForm
from marshmallow import fields, post_load, post_dump
from wtforms.fields import SelectField, FormField

from wazo_admin_ui.helpers.mallow import BaseSchema


_destination_choices = set()
_listing_urls = {}


def register_listing_url(type_id, endpoint):
    _listing_urls[type_id] = endpoint


def register_destination_form(type_id, type_label, form):
    _destination_choices.add((type_id, type_label))
    setattr(DestinationForm, type_id, FormField(form))


class DestinationForm(FlaskForm):
    listing_urls = _listing_urls

    type = SelectField('Destination', choices=_destination_choices)


class DestinationField(FormField):

    def __init__(self, *args, **kwargs):
        super(DestinationField, self).__init__(DestinationForm, *args, **kwargs)


class FallbacksForm(FlaskForm):
    busy_destination = DestinationField('Busy')
    congestion_destination = DestinationField('Congestion')
    fail_destination = DestinationField('Fail')
    noanswer_destination = DestinationField('No answer')


class DestinationSchema(BaseSchema):

    @post_dump(pass_original=True)
    def _dump_dynamic_destination(self, data, raw_data):
        if not isinstance(raw_data, dict):
            return data

        destination_type = raw_data['type']
        result = raw_data[destination_type]
        result['type'] = destination_type
        result.pop('csrf_token', None)
        return result

    @post_load(pass_original=True)
    def _load_dynamic_destination(self, data, raw_data):
        if not isinstance(raw_data, dict):
            return data

        destination_type = raw_data.pop('type')
        result = {'type': destination_type,
                  destination_type: raw_data}
        return result


class FallbacksSchema(BaseSchema):
    busy_destination = fields.Nested(DestinationSchema)
    congestion_destination = fields.Nested(DestinationSchema)
    fail_destination = fields.Nested(DestinationSchema)
    noanswer_destination = fields.Nested(DestinationSchema)
