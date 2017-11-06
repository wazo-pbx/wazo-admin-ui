# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import logging

from flask import redirect
from flask import url_for
from flask.helpers import flash
from wazo_admin_ui.helpers.error import (ErrorExtractor,
                                         ErrorTranslator,
                                         GENERIC_MESSAGE_ERRORS,
                                         GENERIC_PATTERN_ERRORS,
                                         RESOURCES,
                                         URL_TO_NAME_RESOURCES,
                                         SPECIFIC_MESSAGE_ERRORS,
                                         SPECIFIC_PATTERN_ERRORS)

from requests.exceptions import ConnectionError


logger = logging.getLogger(__name__)


def configure_error_handlers(app):

    ErrorExtractor.register_generic_patterns(GENERIC_PATTERN_ERRORS)
    ErrorExtractor.register_specific_patterns(SPECIFIC_PATTERN_ERRORS)
    ErrorExtractor.register_url_to_name_resources(URL_TO_NAME_RESOURCES)
    ErrorTranslator.register_generic_messages(GENERIC_MESSAGE_ERRORS)
    ErrorTranslator.register_specific_messages(SPECIFIC_MESSAGE_ERRORS)
    ErrorTranslator.register_resources(RESOURCES)

    @app.errorhandler(401)
    def page_unauthorized(error):
        return _flash_and_redirect(error)

    @app.errorhandler(403)
    def page_forbidden(error):
        return _flash_and_redirect(error)

    @app.errorhandler(404)
    def page_not_found(error):
        return _flash_and_redirect(error)

    @app.errorhandler(ConnectionError)
    def connection_error(error):
        logger.exception(ConnectionError)
        return _flash_and_redirect(error)

    @app.errorhandler(Exception)
    def exception_handler(error):
        logger.exception(Exception)
        return _flash_and_redirect(error)

    def _flash_and_redirect(error):
        flash(str(error), 'error')
        return redirect(url_for('index.Index:get'))
