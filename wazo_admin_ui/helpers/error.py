# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

import ast
import re
import logging

from flask_babel import lazy_gettext as l_

GENERIC_PATTERN_ERRORS = {
    'resource-not-found': r'^Resource Not Found',
    'invalid-data': r'^Input Error',
}

GENERIC_MESSAGE_ERRORS = {
    'resource-not-found': l_('Resource not found'),
    'invalid-data': l_('Input error'),
}


SPECIFIC_PATTERN_ERRORS = {
    'contains-only': r'One or more of the choices you made was not acceptable',
    'equal': r'Must be equal to',
    'field-format-datetime': r'cannot be formatted as a datetime',
    'field-format-time': r'cannot be formatted as date',
    'field-format-timedelta': r'cannot be formatted as a timedelta',
    'field-invalid-boolean': r'Not a valid boolean',
    'field-invalid-datetime': r'Not a valid datetime',
    'field-invalid-dict': r'Not a valid mapping type',
    'field-invalid-email': r'Not a valid email address',
    'field-invalid-formatted-string': r'Cannot format string with given data',
    'field-invalid-integer': r'Not a valid integer',
    'field-invalid-number': r'Not a valid number',
    'field-invalid-string': r'Not a valid string',
    'field-invalid-time': r'Not a valid time',
    'field-invalid-timedelta': r'Not a valid period of time',
    'field-invalid-url': r'Not a valid URL',
    'field-invalid-uuid': r'Not a valid UUID',
    'field-null': r'Field may not be null',
    'field-required': r'Missing data for required field',
    'field-type': r'Invalid input type',
    'field-validator-failed': r'Invalid value',
    'input': r'Invalid input',
    'length': r'(Shorter than minimum length|Longer than maximum length|Length must be between| Length must be)',
    'oneof': r'Not a valid choice',
    'range': r'(Must be at least|Must be at most|Must be between)',
    'regexp': r'String does not match expected pattern',
}

SPECIFIC_MESSAGE_ERRORS = {
    'contains-only': l_('One or more of the choices you made was not acceptable'),
    'equal': l_('Invalid value'),
    'field-format-datetime': l_('cannot be formatted as a datetime'),
    'field-format-time': l_('cannot be formatted as date'),
    'field-format-timedelta': l_('cannot be formatted as a timedelta'),
    'field-invalid-boolean': l_('Not a valid boolean'),
    'field-invalid-datetime': l_('Not a valid datetime'),
    'field-invalid-dict': l_('Not a valid mapping type'),
    'field-invalid-email': l_('Not a valid email address'),
    'field-invalid-formatted-string': l_('Cannot format string with given data'),
    'field-invalid-integer': l_('Not a valid integer'),
    'field-invalid-number': l_('Not a valid number'),
    'field-invalid-string': l_('Not a valid string'),
    'field-invalid-time': l_('Not a valid time'),
    'field-invalid-timedelta': l_('Not a valid period of time'),
    'field-invalid-url': l_('Not a valid URL'),
    'field-invalid-uuid': l_('Not a valid UUID'),
    'field-null': l_('Field may not be null'),
    'field-required': l_('Missing data for required field'),
    'field-type': l_('Invalid input type'),
    'field-validator-failed': l_('Invalid value'),
    'input': l_('Invalid input'),
    'length': l_('Invalid length'),
    'oneof': l_('Not a valid choice'),
    'range': l_('Invalid range'),
    'regexp': l_('String does not match expected pattern'),
}

URL_TO_NAME_RESOURCES = {
    'callpermissions': 'call_permission',
    'conferences': 'conference',
    'extensions': 'extension',
    'parkinglots': 'parking_lot',
    'switchboards': 'switchboard',
    'users': 'user',
    'voicemails': 'voicemail',
}

RESOURCES = {
    'call_permission': l_('call permission'),
    'conference': l_('conference'),
    'extension': l_('extension'),
    'parking_lot': l_('parking lot'),
    'switchboard': l_('switchboard'),
    'user': l_('user'),
    'voicemail': l_('voicemail'),
}

logger = logging.getLogger(__name__)


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
    url_to_name_resources = {}

    @classmethod
    def register_generic_patterns(cls, patterns):
        cls.generic_patterns.update(patterns)

    @classmethod
    def register_specific_patterns(cls, patterns):
        cls.specific_patterns.update(patterns)

    @classmethod
    def register_url_to_name_resources(cls, resources):
        cls.url_to_name_resources.update(resources)

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
                    break
            else:
                logger.debug('Unable to extract specific error id from: %s', value)

        return result

    @classmethod
    def extract_resource(cls, request):
        # TODO: How to extract sub-resource like /usrs/id/funckeys
        regex = re.compile(RESOURCE_REGEX)
        match = regex.match(request.path_url)
        if not match:
            logger.debug('Unable to extract resource from: %s', request.path_url)
            return None
        url_resource = match.group(1)
        return cls.url_to_name_resources.get(url_resource, url_resource)


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
        logger.debug('Unable to extract generic error id from: %s', response)
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
            logger.debug('Unable to extract field from: %s', message)
            return {}
        key = match.group(1)
        value_str = match.group(2)
        try:
            value = ast.literal_eval(value_str)
        except (ValueError, SyntaxError):
            value = value_str

        return {key: value}
