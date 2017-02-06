# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import logging
import os

from datetime import timedelta

from cherrypy import wsgiserver
from flask import Flask
from flask import request
from flask_babel import Babel
from flask_menu import Menu
from flask_session import Session
from flask_login import LoginManager
from requests.exceptions import HTTPError

from xivo import http_helpers
from xivo.auth_verifier import AuthVerifier

from .errors import configure_error_handlers
from .auth import AuthClient
from .user import UserUI

logger = logging.getLogger(__name__)
app = Flask('wazo_admin_ui')
auth_verifier = AuthVerifier()


class ReverseProxied(object):
    '''
    From http://flask.pocoo.org/snippets/35/
    '''

    def __init__(self, application):
        self.app = application

    def __call__(self, environ, start_response):
        script_name = environ.get('HTTP_X_SCRIPT_NAME', '')
        if script_name:
            environ['SCRIPT_NAME'] = script_name

        return self.app(environ, start_response)


class Server(object):

    def __init__(self, global_config):
        self.config = global_config['https']
        http_helpers.add_logger(app, logger)

        app.after_request(http_helpers.log_request_hide_token)

        app.secret_key = os.urandom(24)
        app.permanent_session_lifetime = timedelta(minutes=60)
        AuthClient.set_config(global_config['auth'])

        configure_error_handlers(app)
        self._configure_login()
        self._configure_babel()
        self._configure_menu()
        self._configure_session(global_config['session_file_dir'])

    def get_app(self):
        return app

    def run(self):
        bind_addr = (self.config['listen'], self.config['port'])

        wsgi_app = ReverseProxied(wsgiserver.WSGIPathInfoDispatcher({'/': app}))
        self.server = wsgiserver.CherryPyWSGIServer(bind_addr=bind_addr,
                                                    wsgi_app=wsgi_app)
        self.server.ssl_adapter = http_helpers.ssl_adapter(self.config['certificate'],
                                                           self.config['private_key'],
                                                           self.config['ciphers'])
        logger.debug('WSGIServer starting... uid: %s, listen: %s:%s', os.getuid(), bind_addr[0], bind_addr[1])
        for route in http_helpers.list_routes(app):
            logger.debug(route)

        try:
            self.server.start()
        except KeyboardInterrupt:
            self.server.stop()

    def stop(self):
        if self.server:
            self.server.stop()

    def _configure_login(self):
        login_manager = LoginManager()
        login_manager.init_app(app)

        @login_manager.user_loader
        def load_token(token):
            try:
                response = AuthClient().token.get(token)
            except HTTPError:
                return None
            token = response.get('token')
            if not token:
                return None
            return UserUI(token)

    def _configure_menu(self):
        menu = Menu()
        menu.init_app(app)

    def _configure_babel(self):
        babel = Babel()
        babel.init_app(app)
        app.config['BABEL_DEFAULT_LOCALE'] = 'en'

        @babel.localeselector
        def get_locale():
            translations = [str(translation) for translation in babel.list_translations()]
            return request.accept_languages.best_match(translations)

    def _configure_session(self, session_file_dir):
        app.config['SESSION_FILE_DIR'] = session_file_dir
        app.config['SESSION_TYPE'] = 'filesystem'
        sess = Session()
        sess.init_app(app)