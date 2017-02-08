# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask import Blueprint
from flask_menu.classy import register_flaskview


from .service import ConferenceService
from .view import ConferenceView

conference = Blueprint('conference', __name__, template_folder='templates',
                       static_folder='static', static_url_path='/%s' % __name__)


class Plugin(object):

    def load(self, dependencies):
        core = dependencies['flask']
        config = dependencies['config']

        ConferenceView.service = ConferenceService(config['confd'])
        ConferenceView.register(conference, route_base='/conferences')
        register_flaskview(conference, ConferenceView)

        core.register_blueprint(conference)
