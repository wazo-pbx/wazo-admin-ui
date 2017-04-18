# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from werkzeug.datastructures import ImmutableMultiDict
from wtforms.fields import SelectField, FormField, HiddenField, StringField
from wtforms.utils import unset_value

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
        self.destination_choices = list(_destination_choices)
        super(DestinationForm, self).__init__(*args, **kwargs)
        self.type.choices = [('none', 'None')] + self.destination_choices
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
        destination_type = kwargs.pop('type', None)
        destination_args = kwargs
        wrapped_formdata = self.meta.wrap_formdata(self, formdata)
        if wrapped_formdata and isinstance(wrapped_formdata, ImmutableMultiDict):
            destination_type = wrapped_formdata.get(self._prefix + 'type', '')
            key_prefix = self._prefix + destination_type + '-'
            destination_args = {k[len(key_prefix):]: v for k, v in wrapped_formdata.iteritems() if key_prefix in k}

        if destination_type:
            kwargs = {'type': destination_type,
                      destination_type: destination_args}
            if not getattr(self, destination_type, False) and destination_type != 'none':
                self._create_dynamic_destination_form(kwargs)

        super(DestinationForm, self).process(formdata, obj, data, **kwargs)

    def _create_dynamic_destination_form(self, destination):
        class DynamicForm(BaseForm):
            pass

        for key in destination[destination['type']]:
            setattr(DynamicForm, key, StringField())

        options = dict(name=destination['type'],
                       prefix=self._prefix,
                       translations=self.meta.get_translations(self))
        field = self.meta.bind_field(self, FormField(DynamicForm), options)
        self._fields[destination['type']] = field
        self.destination_choices.append((destination['type'], destination['type']))


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
