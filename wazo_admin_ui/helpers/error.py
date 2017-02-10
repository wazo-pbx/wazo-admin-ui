# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

import ast
import re

from flask_babel import lazy_gettext

GENERIC_PATTERN_ERRORS = {'resource-not-found': r'^Resource Not Found',
                          'invalid-data': r'^Input Error'}

GENERIC_MESSAGE_ERRORS = {'resource-not-found': lazy_gettext('Resource not found'),
                          'invalid-data': lazy_gettext('Input error')}


SPECIFIC_PATTERN_ERRORS = {'required-field': r'Missing data for required field',
                           'invalid-choice': r'Not a valid choice',
                           'invalid-length': r'Longer than maximum length'}

SPECIFIC_MESSAGE_ERRORS = {'required-field': lazy_gettext('Missing data for required field'),
                           'invalid-choice': lazy_gettext('Not a valid choice'),
                           'invalid-length': lazy_gettext('Longer than maximum length')}

RESOURCES = {'conferences': lazy_gettext('conference'),
             'users': lazy_gettext('user')}


class ErrorTranslator(object):
    generic_messages = {}
    specific_messages = {}
    resources = {}

    @classmethod
    def register_generic_messages(cls, messages):
        cls.generic_messages.update(messages)

    @classmethod
    def register_specific_messages(cls, messages):
        cls.specific_messages.update(messages)

    @classmethod
    def register_resources(cls, resources):
        cls.resources.update(resources)

    # Maybe should be in a manager?
    @classmethod
    def translate_specific_error_id_from_fields(cls, fields):
        result = {}
        for field, value in fields.iteritems():
            if isinstance(value, dict):
                result[field] = cls.translate_specific_error_id_from_fields(value)
                continue
            result[field] = cls.specific_messages.get(value)
        return result


# Match
# /1.1/users
# /1.1/users/id
# Do not match:
# /1.1/users/id/funckeys
RESOURCE_REGEX = r'^/[^/]+/([^/]+)(?:/[^/]+)?$'


class ErrorExtractor(object):

    generic_patterns = {}
    specific_patterns = {}

    @classmethod
    def register_generic_patterns(cls, patterns):
        cls.generic_patterns.update(patterns)

    @classmethod
    def register_specific_patterns(cls, patterns):
        cls.specific_patterns.update(patterns)

    @classmethod
    def extract_specific_error_id_from_fields(cls, fields):
        # Allow only 1 error_id by field
        result = {}
        for field, value in fields.iteritems():
            if isinstance(value, dict):
                result[field] = cls.extract_specific_error_id_from_fields(value)
                continue
            if isinstance(value, list):
                try:
                    value = ', '.join(value)
                except TypeError:
                    pass

            if not isinstance(value, unicode):
                value = unicode(value)

            for error_id, pattern in cls.specific_patterns.iteritems():
                regex = re.compile(pattern)
                if regex.search(value):
                    result[field] = error_id
        return result

    @classmethod
    def extract_resource(cls, request):
        # TODO: How to extract sub-resource like /usrs/id/funckeys
        regex = re.compile(RESOURCE_REGEX)
        match = regex.match(request.path_url)
        if match:
            return match.group(1)
        return None


class ConfdErrorExtractor(ErrorExtractor):

    specific_field_regex = r'^.* - ([^:]*): (.*)$'

    @classmethod
    def extract_generic_error_id(cls, response):
        if not isinstance(response, list):
            return None

        for error_id, pattern in cls.generic_patterns.iteritems():
            regex = re.compile(pattern)
            for message in response:
                if regex.search(message):
                    return error_id
        return None

    @classmethod
    def extract_fields(cls, response):
        result = {}
        for message in response:
            field = cls.extract_field(message)
            result.update(field)
        return result

    @classmethod
    def extract_field(cls, message):
        regex = re.compile(cls.specific_field_regex)
        match = regex.match(message)
        if not match:
            return {}
        key = match.group(1)
        value_str = match.group(2)
        try:
            value = ast.literal_eval(value_str)
        except (ValueError, SyntaxError):
            value = value_str

        return {key: value}
